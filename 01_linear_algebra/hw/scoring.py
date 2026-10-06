"""Fail-closed pytest execution shared by the active assignment's scorers."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


class ScoringError(RuntimeError):
    """The test run cannot be interpreted as a completed student score."""


def run_verified_pytest(
    expected_inventory: list[str], marker: str | None = None
) -> dict:
    """Collect and execute identical inventories using fresh, private JSON reports.

    Assertion failures are valid student outcomes. Collection, setup/teardown,
    skipped tests, missing reports, and interrupted processes are not grades.
    """
    cwd = Path.cwd()
    expected = set(expected_inventory)
    if not expected or len(expected) != len(expected_inventory):
        raise ScoringError("Expected test inventory is empty or duplicated")
    files = sorted({item.split("::")[0] for item in expected})
    with tempfile.TemporaryDirectory(prefix="course-score-") as temporary:
        root = Path(temporary)
        (root / "course_inventory_plugin.py").write_text(
            "import json, os\n"
            "from pathlib import Path\n"
            "def pytest_collection_finish(session):\n"
            "    Path(os.environ['COURSE_INVENTORY_REPORT']).write_text(\n"
            "        json.dumps([item.nodeid for item in session.items]))\n"
        )

        def run(
            name: str, extra: list[str]
        ) -> tuple[subprocess.CompletedProcess, dict]:
            report_path = root / f"{name}.json"
            inventory_path = root / f"{name}-inventory.json"
            environment = dict(os.environ)
            environment["PYTHONPATH"] = (
                str(root) + os.pathsep + environment.get("PYTHONPATH", "")
            )
            environment["COURSE_INVENTORY_REPORT"] = str(inventory_path)
            command = [
                sys.executable,
                "-m",
                "pytest",
                "-p",
                "course_inventory_plugin",
                *files,
                "--json-report",
                f"--json-report-file={report_path}",
                "-q",
                "--tb=short",
                *extra,
            ]
            if marker:
                command += ["-m", marker]
            try:
                process = subprocess.run(
                    command,
                    cwd=cwd,
                    env=environment,
                    capture_output=True,
                    text=True,
                    timeout=900,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise ScoringError(f"pytest {name} did not complete: {exc}") from exc
            if process.returncode not in ({0} if name == "collection" else {0, 1}):
                raise ScoringError(
                    f"pytest {name} exited {process.returncode}: "
                    f"{(process.stdout + process.stderr)[-1200:]}"
                )
            try:
                report = json.loads(report_path.read_text())
                report["selected_inventory"] = json.loads(inventory_path.read_text())
            except (OSError, ValueError) as exc:
                raise ScoringError(
                    f"pytest {name} produced no valid fresh report"
                ) from exc
            if report.get("exitcode") != process.returncode:
                raise ScoringError(
                    "pytest report exit status disagrees with its process"
                )
            if any(c.get("outcome") == "failed" for c in report.get("collectors", [])):
                raise ScoringError("pytest collection failed")
            return process, report

        _, collection = run("collection", ["--collect-only"])
        collected = collection["selected_inventory"]
        inventory = set(collected)
        if not inventory or len(inventory) != len(collected):
            raise ScoringError("pytest collected no tests or duplicated test IDs")
        if (not marker and inventory != expected) or not inventory <= expected:
            raise ScoringError(
                f"Test inventory changed: missing={sorted(expected - inventory)}, "
                f"unexpected={sorted(inventory - expected)}"
            )
        process, report = run("execution", [])
        if report["selected_inventory"] != collected:
            raise ScoringError(
                "Selected inventory changed between collection and execution"
            )
        tests = report.get("tests", [])
        if Counter(t.get("nodeid") for t in tests) != Counter(collected):
            raise ScoringError("Executed tests do not match collected tests")
        for test in tests:
            if test.get("outcome") not in {"passed", "failed"}:
                raise ScoringError(
                    f"Unscorable outcome for {test.get('nodeid')}: {test.get('outcome')}"
                )
            if any(
                test.get(phase, {}).get("outcome") != "passed"
                for phase in ("setup", "teardown")
            ):
                raise ScoringError(f"Setup/teardown failed for {test.get('nodeid')}")
            if test.get("call", {}).get("outcome") not in {"passed", "failed"}:
                raise ScoringError(f"Test body did not complete: {test.get('nodeid')}")
        has_failure = any(t["outcome"] == "failed" for t in tests)
        if (process.returncode == 1) != has_failure:
            raise ScoringError("pytest process status does not match test outcomes")
        report["verification"] = {
            "status": "completed",
            "inventory": sorted(inventory),
            "tests_collected": len(inventory),
            "tests_executed": len(tests),
            "pytest_exitcode": process.returncode,
        }
        return report
