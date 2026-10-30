"""Local scoring — run with: uv run python score.py [group]

Shows your current score grouped by section. A section earns its full
points only when ALL tests in that section pass.

Examples:
    uv run python score.py                        # score everything
    uv run python score.py manual                 # Part 1 (manual derivatives)
    uv run python score.py autograd               # Part 2 (autograd)
    uv run python score.py --zip                  # build hw02_submission.zip for submission
    uv run python score.py --gradescope <path>    # write Gradescope results.json
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

# A released package carries its helper beside this file. The teacher source
# imports the canonical package instead of searching for an unrelated scoring
# module on sys.path (which may belong to another assignment or test fixture).
bundled_helper = Path(__file__).with_name("scoring.py")
if bundled_helper.is_file():
    helper_spec = importlib.util.spec_from_file_location("hw02_bundled_scoring", bundled_helper)
    if helper_spec is None or helper_spec.loader is None:
        raise ImportError(f"Cannot load bundled scoring helper: {bundled_helper}")
    scoring_helper = importlib.util.module_from_spec(helper_spec)
    helper_spec.loader.exec_module(scoring_helper)
else:
    teacher_root = str(Path(__file__).resolve().parents[2])
    sys.path.insert(0, teacher_root)
    try:
        scoring_helper = importlib.import_module("course_tools.scoring")
    finally:
        sys.path.remove(teacher_root)
ScoringError = scoring_helper.ScoringError
run_verified_pytest = scoring_helper.run_verified_pytest

# Points per test class. Every test in a class must pass to earn credit.
POINTS: dict[str, int] = {
    # Part 1: Manual derivatives (45 pts)
    "TestManualGradientQuadratic": 15,
    "TestManualGradientComposite": 15,
    "TestManualPartialGradients": 15,
    # Part 2: Autograd (45 pts)
    "TestAutogradGradientQuadratic": 15,
    "TestAutogradGradientComposite": 15,
    "TestAutogradPartialGradients": 15,
}

WRITEUP_POINTS = 10

# Final grade weighting: raw autograded points scale to 90% of the grade and
# the writeup to 10%, regardless of what the raw point totals sum to.
AUTOGRADED_WEIGHT = 90
WRITEUP_WEIGHT = 10


def weighted_autograded(earned: int, possible: int) -> float:
    """Scale raw autograded points to the 90-point grade weight."""
    return round(AUTOGRADED_WEIGHT * earned / possible, 1) if possible else 0.0


SECTIONS: list[tuple[str, list[str]]] = [
    (
        "Part 1: Manual derivatives",
        [
            "TestManualGradientQuadratic",
            "TestManualGradientComposite",
            "TestManualPartialGradients",
        ],
    ),
    (
        "Part 2: Autograd",
        [
            "TestAutogradGradientQuadratic",
            "TestAutogradGradientComposite",
            "TestAutogradPartialGradients",
        ],
    ),
]

# Teacher-owned expected inventory; changes require an explicit test review.
EXPECTED_INVENTORY = [
    "test_derivatives.py::TestManualGradientQuadratic::test_pure_quadratic",
    "test_derivatives.py::TestManualGradientQuadratic::test_with_linear_term",
    "test_derivatives.py::TestManualGradientQuadratic::test_negative_coefficients",
    "test_derivatives.py::TestManualGradientQuadratic::test_at_zero",
    "test_derivatives.py::TestManualGradientQuadratic::test_fractional_coefficients",
    "test_derivatives.py::TestManualGradientComposite::test_at_one",
    "test_derivatives.py::TestManualGradientComposite::test_at_zero",
    "test_derivatives.py::TestManualGradientComposite::test_at_two",
    "test_derivatives.py::TestManualGradientComposite::test_negative_input",
    "test_derivatives.py::TestManualPartialGradients::test_basic_point",
    "test_derivatives.py::TestManualPartialGradients::test_at_origin",
    "test_derivatives.py::TestManualPartialGradients::test_asymmetric_point",
    "test_derivatives.py::TestManualPartialGradients::test_returns_tuple",
    "test_derivatives.py::TestAutogradGradientQuadratic::test_matches_manual",
    "test_derivatives.py::TestAutogradGradientQuadratic::test_with_linear_term",
    "test_derivatives.py::TestAutogradGradientQuadratic::test_negative_coefficients",
    "test_derivatives.py::TestAutogradGradientQuadratic::test_returns_float",
    "test_derivatives.py::TestAutogradGradientComposite::test_matches_manual",
    "test_derivatives.py::TestAutogradGradientComposite::test_at_zero",
    "test_derivatives.py::TestAutogradGradientComposite::test_at_two",
    "test_derivatives.py::TestAutogradGradientComposite::test_returns_float",
    "test_derivatives.py::TestAutogradPartialGradients::test_matches_manual",
    "test_derivatives.py::TestAutogradPartialGradients::test_at_origin",
    "test_derivatives.py::TestAutogradPartialGradients::test_asymmetric_point",
    "test_derivatives.py::TestAutogradPartialGradients::test_returns_tuple_of_floats",
]

SUBMISSION_FILES: list[str] = ["derivatives.py", "writeup.md"]
ZIP_NAME = "hw02_submission.zip"


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
    print("Upload this file using the HW02 submission instructions.")


def run_pytest(marker_filter: str | None = None) -> dict:
    return run_verified_pytest(EXPECTED_INVENTORY, marker_filter)


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
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    output = None
    if mode in {"--gradescope", "--verification-json"}:
        if len(sys.argv) != 3:
            raise SystemExit(f"Usage: score.py {mode} PATH")
        output = Path(sys.argv[2])
        output.unlink(missing_ok=True)  # a failed run must never leave an old grade
    try:
        report = run_pytest(None if output else mode)
        by_class = collect_results(report)
        selected = {node.split("::")[1] for node in report["verification"]["inventory"]}
        if not selected <= set(POINTS) or (mode is None or output) and selected != set(POINTS):
            raise ScoringError("Scored class inventory does not match POINTS")
    except ScoringError as exc:
        print(f"Scoring could not complete: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    if mode == "--gradescope":
        assert output is not None
        write_gradescope_results(by_class, str(output))
    elif mode == "--verification-json":
        assert output is not None
        earned = sum(
            POINTS[c]
            for c, info in by_class.items()
            if info["total"] > 0 and info["passed"] == info["total"]
        )
        receipt = dict(
            report["verification"],
            raw_score=earned,
            raw_max=sum(POINTS.values()),
            weighted_score=weighted_autograded(earned, sum(POINTS.values())),
            classes=by_class,
        )
        output.write_text(json.dumps(receipt, indent=2))
    else:
        print_score(by_class)


if __name__ == "__main__":
    main()
