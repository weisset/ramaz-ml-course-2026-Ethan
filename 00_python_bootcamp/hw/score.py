"""Local scoring — run with: uv run python score.py [group]

Shows your current score grouped by section. A section earns its full
points only when ALL tests in that section pass.

Examples:
    uv run python score.py                        # score everything
    uv run python score.py lists                  # only Part 1 (Lists)
    uv run python score.py dicts                  # only Part 2 (Dicts)
    uv run python score.py sets                   # only Part 3 (Sets)
    uv run python score.py hof                    # only Part 4 (Higher-order functions)
    uv run python score.py classes                # only Part 5 (Classes)
    uv run python score.py songs                  # only Part 6 (Songs)
    uv run python score.py --zip                  # build hw00_submission.zip for Drive upload
    uv run python score.py --gradescope <path>    # write Gradescope results.json
"""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

# Points per test class. Every test in a class must pass to earn credit.
POINTS: dict[str, int] = {
    # Part 1: Lists (17 pts)
    "TestFlatten": 2,
    "TestMostFrequent": 2,
    "TestRunningAverage": 3,
    "TestChunk": 2,
    "TestRotate": 2,
    "TestRunLengthEncode": 3,
    "TestSlidingWindow": 3,
    # Part 2: Dicts (13 pts)
    "TestCountOccurrences": 2,
    "TestInvertDict": 1,
    "TestGroupBy": 3,
    "TestDeepGet": 4,
    "TestTwoSum": 3,
    # Part 3: Sets (5 pts)
    "TestFindDuplicates": 2,
    "TestJaccardSimilarity": 3,
    # Part 4: Higher-order functions (11 pts)
    "TestApplyTwice": 1,
    "TestMakeMultiplier": 2,
    "TestPipeline": 4,
    "TestMemoize": 4,
    # Part 5: Classes (10 pts)
    "TestStudent": 5,
    "TestGradebook": 5,
    # Part 6: Analysis (17 pts)
    "TestLoadSongs": 2,
    "TestSongRanker": 4,
    "TestAvgWeeksByGenre": 3,
    "TestMostStreamedArtist": 4,
    "TestHitsPerYear": 4,
}

SECTIONS: list[tuple[str, list[str]]] = [
    (
        "Part 1: Lists",
        [
            "TestFlatten",
            "TestMostFrequent",
            "TestRunningAverage",
            "TestChunk",
            "TestRotate",
            "TestRunLengthEncode",
            "TestSlidingWindow",
        ],
    ),
    (
        "Part 2: Dicts",
        [
            "TestCountOccurrences",
            "TestInvertDict",
            "TestGroupBy",
            "TestDeepGet",
            "TestTwoSum",
        ],
    ),
    (
        "Part 3: Sets",
        ["TestFindDuplicates", "TestJaccardSimilarity"],
    ),
    (
        "Part 4: Higher-order functions",
        ["TestApplyTwice", "TestMakeMultiplier", "TestPipeline", "TestMemoize"],
    ),
    (
        "Part 5: Classes",
        ["TestStudent", "TestGradebook"],
    ),
    (
        "Part 6: Analysis",
        [
            "TestLoadSongs",
            "TestSongRanker",
            "TestAvgWeeksByGenre",
            "TestMostStreamedArtist",
            "TestHitsPerYear",
        ],
    ),
]

WRITEUP_POINTS = 15

# Final grade weighting: raw autograded points scale to 90% of the grade and
# the writeup to 10%, regardless of what the raw point totals sum to.
AUTOGRADED_WEIGHT = 90
WRITEUP_WEIGHT = 10


def weighted_autograded(earned: int, possible: int) -> float:
    """Scale raw autograded points to the 90-point grade weight."""
    return round(AUTOGRADED_WEIGHT * earned / possible, 1) if possible else 0.0


REPORT_FILE = Path(".report.json")

SUBMISSION_FILES: list[str] = ["python_basics.py", "analysis.py", "writeup.md"]
ZIP_NAME = "hw00_submission.zip"


def build_zip() -> None:
    """Build the submission zip with the right files at the right level."""
    missing = [f for f in SUBMISSION_FILES if not Path(f).exists()]
    if missing:
        print("Cannot build the submission zip — missing file(s):")
        for f in missing:
            print(f"  - {f}")
        print("Run this command from the hw/ directory, with all files present.")
        sys.exit(1)
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in SUBMISSION_FILES:
            zf.write(f)
    print(f"Created {ZIP_NAME} containing: {', '.join(SUBMISSION_FILES)}")
    print("Rename it to lastname_firstname_hw00.zip and upload it to the HW00 Drive folder.")


def run_pytest(marker_filter: str | None = None) -> None:
    cmd = [
        "uv",
        "run",
        "pytest",
        "--json-report",
        f"--json-report-file={REPORT_FILE}",
        "-q",
        "--tb=no",
    ]
    if marker_filter:
        cmd += ["-m", marker_filter]
    subprocess.run(cmd, capture_output=True)


def load_report() -> dict:
    return json.loads(REPORT_FILE.read_text())


def parse_class_name(nodeid: str) -> str | None:
    parts = nodeid.split("::")
    return parts[1] if len(parts) >= 2 else None


def collect_results(report: dict) -> dict[str, dict]:
    """Group test outcomes by class name."""
    by_class: dict[str, dict] = {}
    for test in report.get("tests", []):
        cls = parse_class_name(test["nodeid"])
        if cls is None or cls not in POINTS:
            continue
        if cls not in by_class:
            by_class[cls] = {"passed": 0, "total": 0, "failures": []}
        by_class[cls]["total"] += 1
        if test["outcome"] == "passed":
            by_class[cls]["passed"] += 1
        else:
            method = test["nodeid"].split("::")[-1]
            by_class[cls]["failures"].append(method)
    return by_class


def print_score(by_class: dict[str, dict]) -> None:
    total_earned = 0
    total_possible = 0

    print()
    for section_name, classes in SECTIONS:
        sec_earned = 0
        sec_possible = sum(POINTS[c] for c in classes if c in POINTS)
        lines: list[str] = []

        for cls in classes:
            pts = POINTS[cls]
            if cls not in by_class:
                lines.append(f"  [ -- ] {cls}: not run")
                continue

            info = by_class[cls]
            all_pass = info["passed"] == info["total"]
            earned = pts if all_pass else 0
            sec_earned += earned

            tag = "PASS" if all_pass else "FAIL"
            detail = (
                f"  [{tag}] {cls}: {earned}/{pts}"
                if all_pass
                else f"  [{tag}] {cls}: 0/{pts}  ({info['passed']}/{info['total']} tests passed)"
            )
            lines.append(detail)
            for f in info["failures"]:
                lines.append(f"         x {f}")

        total_earned += sec_earned
        total_possible += sec_possible

        print(f"{section_name}  [{sec_earned}/{sec_possible}]")
        for line in lines:
            print(line)
        print()

    print("=" * 50)
    print(f"  TOTAL SCORE (autograded):  {total_earned} / {total_possible}")
    weighted = weighted_autograded(total_earned, total_possible)
    print(f"  Weighted (90% of grade):   {weighted} / {AUTOGRADED_WEIGHT}")
    print(
        f"  Note: writeup.md is graded separately "
        f"(raw {WRITEUP_POINTS} pts, worth {WRITEUP_WEIGHT}% of the grade)."
    )
    print()


def write_gradescope_results(by_class: dict[str, dict], output_path: str) -> None:
    """Write Gradescope results.json from collected test results."""
    tests: list[dict] = []
    total = 0
    autograded_total = sum(POINTS.values())

    for _, classes in SECTIONS:
        for cls in classes:
            pts = POINTS[cls]
            info = by_class.get(cls, {})
            passed = info.get("passed", 0)
            n_tests = info.get("total", 0)
            all_pass = n_tests > 0 and passed == n_tests
            score = pts if all_pass else 0
            total += score

            if all_pass:
                detail = f"All {passed} test(s) passed."
            elif n_tests == 0:
                detail = (
                    "No tests ran — make sure the function is implemented "
                    "and does not raise NotImplementedError."
                )
            else:
                detail = f"{passed}/{n_tests} test(s) passed."
                failures = info.get("failures", [])
                if failures:
                    detail += "\nFailing: " + ", ".join(failures[:5])

            tests.append(
                {
                    "score": score,
                    "max_score": pts,
                    "name": cls.removeprefix("Test"),
                    "output": detail,
                    "visibility": "visible",
                }
            )

    weighted = weighted_autograded(total, autograded_total)
    results = {
        "score": weighted,
        "output": (
            f"Raw autograded score: {total}/{autograded_total}\n"
            f"Scaled to {AUTOGRADED_WEIGHT}% of the grade: "
            f"{AUTOGRADED_WEIGHT} x ({total}/{autograded_total}) = "
            f"{weighted}/{AUTOGRADED_WEIGHT}\n"
            f"(writeup graded separately, worth {WRITEUP_WEIGHT}% of the grade)"
        ),
        "tests": tests,
    }
    Path(output_path).write_text(json.dumps(results, indent=2))
    print(
        f"Wrote {output_path}  (raw {total}/{autograded_total} -> {weighted}/{AUTOGRADED_WEIGHT})"
    )


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "--zip":
        build_zip()
        return

    if len(sys.argv) >= 3 and sys.argv[1] == "--gradescope":
        run_pytest()
        if not REPORT_FILE.exists():
            print("Error: could not generate test report.")
            sys.exit(1)
        report = load_report()
        by_class = collect_results(report)
        write_gradescope_results(by_class, sys.argv[2])
        return

    marker = sys.argv[1] if len(sys.argv) > 1 else None
    run_pytest(marker)

    if not REPORT_FILE.exists():
        print("Error: could not generate test report.")
        print("Make sure pytest-json-report is installed: uv sync")
        sys.exit(1)

    report = load_report()
    by_class = collect_results(report)
    print_score(by_class)


if __name__ == "__main__":
    main()
