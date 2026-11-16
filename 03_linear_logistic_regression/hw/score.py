"""Score calculator for HW03.

Run this script to see your current score before submitting.

Usage:
    uv run python score.py                        # full report
    uv run python score.py methods                # method tests only
    uv run python score.py pipeline               # pipeline tests only
    uv run python score.py experiments            # experiment-helper tests only
    uv run python score.py --zip                  # build hw03_submission.zip for submission
    uv run python score.py --gradescope <path>    # write Gradescope results.json
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path
from typing import TypedDict

# Published homework and grader archives carry the shared scorer beside this file.
bundled_helper = Path(__file__).with_name("scoring.py")
if bundled_helper.is_file():
    helper_spec = importlib.util.spec_from_file_location("hw03_bundled_scoring", bundled_helper)
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

# Every test in a class must pass to earn its points.
POINTS: dict[str, int] = {
    "TestSigmoid": 5,
    "TestLinearInit": 3,
    "TestLinearForward": 4,
    "TestLinearLoss": 4,
    "TestLinearGradient": 6,
    "TestLogisticInit": 3,
    "TestLogisticForward": 4,
    "TestLogisticLoss": 5,
    "TestLogisticGradient": 6,
    "TestLinearFit": 10,
    "TestLinearPredict": 3,
    "TestLogisticFit": 10,
    "TestLogisticPredict": 7,
    "TestLoadRegressionData": 4,
    "TestTrainLinearModel": 4,
    "TestLoadClassificationData": 4,
    "TestMajorityClassBaseline": 4,
    "TestTrainLogisticModel": 4,
}

SECTIONS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "methods": (
        "Method tests (40 pts)",
        [
            ("TestSigmoid", "sigmoid"),
            ("TestLinearInit", "LinearRegression.__init__"),
            ("TestLinearForward", "LinearRegression.forward"),
            ("TestLinearLoss", "LinearRegression.loss"),
            ("TestLinearGradient", "LinearRegression.gradient"),
            ("TestLogisticInit", "LogisticRegression.__init__"),
            ("TestLogisticForward", "LogisticRegression.forward"),
            ("TestLogisticLoss", "LogisticRegression.loss"),
            ("TestLogisticGradient", "LogisticRegression.gradient"),
        ],
    ),
    "pipeline": (
        "Pipeline tests (30 pts)",
        [
            ("TestLinearFit", "LinearRegression.fit"),
            ("TestLinearPredict", "LinearRegression.predict"),
            ("TestLogisticFit", "LogisticRegression.fit"),
            ("TestLogisticPredict", "LogisticRegression.predict / predict_proba"),
        ],
    ),
    "experiments": (
        "Experiment tests (20 pts)",
        [
            ("TestLoadRegressionData", "load_regression_data"),
            ("TestTrainLinearModel", "train_linear_model"),
            ("TestLoadClassificationData", "load_classification_data"),
            ("TestMajorityClassBaseline", "majority_class_baseline"),
            ("TestTrainLogisticModel", "train_logistic_model"),
        ],
    ),
}

# Only public scored tests are included. Teacher-side guard tests run separately.
EXPECTED_INVENTORY = [
    "test_regression.py::TestSigmoid::test_at_zero",
    "test_regression.py::TestSigmoid::test_large_positive",
    "test_regression.py::TestSigmoid::test_large_negative",
    "test_regression.py::TestSigmoid::test_output_in_zero_one",
    "test_regression.py::TestSigmoid::test_symmetry",
    "test_regression.py::TestSigmoid::test_shape_preserved",
    "test_regression.py::TestLinearInit::test_w_shape_and_zeros",
    "test_regression.py::TestLinearInit::test_b_scalar_zero",
    "test_regression.py::TestLinearInit::test_lr_stored",
    "test_regression.py::TestLinearInit::test_default_lr",
    "test_regression.py::TestLinearInit::test_subclasses_linear_model",
    "test_regression.py::TestLinearForward::test_basic",
    "test_regression.py::TestLinearForward::test_batch",
    "test_regression.py::TestLinearForward::test_output_shape",
    "test_regression.py::TestLinearForward::test_zero_weights",
    "test_regression.py::TestLinearLoss::test_perfect",
    "test_regression.py::TestLinearLoss::test_known_value",
    "test_regression.py::TestLinearLoss::test_scalar",
    "test_regression.py::TestLinearLoss::test_non_negative",
    "test_regression.py::TestLinearGradient::test_zero_at_minimum",
    "test_regression.py::TestLinearGradient::test_shapes",
    "test_regression.py::TestLinearGradient::test_matches_formula",
    "test_regression.py::TestLinearGradient::test_direction",
    "test_regression.py::TestLogisticInit::test_w_zeros",
    "test_regression.py::TestLogisticInit::test_b_scalar_zero",
    "test_regression.py::TestLogisticInit::test_default_lr",
    "test_regression.py::TestLogisticInit::test_subclasses_linear_model",
    "test_regression.py::TestLogisticForward::test_zero_params_gives_half",
    "test_regression.py::TestLogisticForward::test_in_zero_one",
    "test_regression.py::TestLogisticForward::test_shape",
    "test_regression.py::TestLogisticForward::test_forward_equals_sigmoid_of_linear_combination",
    "test_regression.py::TestLogisticLoss::test_near_perfect",
    "test_regression.py::TestLogisticLoss::test_scalar",
    "test_regression.py::TestLogisticLoss::test_non_negative",
    "test_regression.py::TestLogisticLoss::test_log_two_at_half",
    "test_regression.py::TestLogisticLoss::test_confident_wrong_penalized",
    "test_regression.py::TestLogisticGradient::test_zero_at_residual_zero",
    "test_regression.py::TestLogisticGradient::test_shapes",
    "test_regression.py::TestLogisticGradient::test_matches_formula",
    "test_regression.py::TestLinearFit::test_loss_history_shape",
    "test_regression.py::TestLinearFit::test_loss_decreases",
    "test_regression.py::TestLinearFit::test_recovers_coefficients",
    "test_regression.py::TestLinearPredict::test_predict_equals_forward",
    "test_regression.py::TestLinearPredict::test_predict_shape",
    "test_regression.py::TestLogisticFit::test_loss_history_shape",
    "test_regression.py::TestLogisticFit::test_loss_decreases",
    "test_regression.py::TestLogisticFit::test_classifies_separable",
    "test_regression.py::TestLogisticPredict::test_proba_in_zero_one",
    "test_regression.py::TestLogisticPredict::test_proba_equals_forward",
    "test_regression.py::TestLogisticPredict::test_predict_threshold",
    "test_regression.py::TestLogisticPredict::test_predict_values_in_zero_one",
    "test_regression.py::TestLoadRegressionData::test_returns_four_tensors",
    "test_regression.py::TestLoadRegressionData::test_dtype_float32",
    "test_regression.py::TestLoadRegressionData::test_shapes",
    "test_regression.py::TestLoadRegressionData::test_no_nans",
    "test_regression.py::TestTrainLinearModel::test_returns_model_and_history",
    "test_regression.py::TestTrainLinearModel::test_loss_decreases",
    "test_regression.py::TestTrainLinearModel::test_model_w_shape",
    "test_regression.py::TestLoadClassificationData::test_returns_four_tensors",
    "test_regression.py::TestLoadClassificationData::test_dtype_float32",
    "test_regression.py::TestLoadClassificationData::test_features_two",
    "test_regression.py::TestLoadClassificationData::test_labels_binary",
    "test_regression.py::TestMajorityClassBaseline::test_balanced",
    "test_regression.py::TestMajorityClassBaseline::test_imbalanced",
    "test_regression.py::TestMajorityClassBaseline::test_majority_is_class_one",
    "test_regression.py::TestMajorityClassBaseline::test_single_class",
    "test_regression.py::TestMajorityClassBaseline::test_returns_python_float",
    "test_regression.py::TestMajorityClassBaseline::test_on_iris_test_split",
    "test_regression.py::TestTrainLogisticModel::test_returns_model_and_history",
    "test_regression.py::TestTrainLogisticModel::test_loss_decreases",
    "test_regression.py::TestTrainLogisticModel::test_classifies_iris",
]

WRITEUP_POINTS = 13
AUTOGRADED_WEIGHT = 90
WRITEUP_WEIGHT = 10
SUBMISSION_FILES = ["regression.py", "analysis.py", "writeup.md"]
ZIP_NAME = "hw03_submission.zip"


class ClassResult(TypedDict):
    passed: int
    total: int
    failures: list[str]
    first_failure: str


def weighted_autograded(earned: int, possible: int) -> float:
    """Scale raw autograded points to the 90-point grade weight."""
    return round(AUTOGRADED_WEIGHT * earned / possible, 1)


def build_zip() -> None:
    """Build the submission zip with the right files at the right level."""
    missing = [name for name in SUBMISSION_FILES if not Path(name).is_file()]
    if missing:
        print("Cannot build the submission zip. Missing files:")
        for name in missing:
            print(f"  - {name}")
        raise SystemExit("Run this command from the hw/ directory, with all files present.")
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in SUBMISSION_FILES:
            archive.write(name)
    print(f"Created {ZIP_NAME} containing: {', '.join(SUBMISSION_FILES)}")
    print("Follow the HW03 README to rename this file and upload it to the Drive folder.")


def class_results(report: dict, marker: str | None) -> dict[str, ClassResult]:
    """Check the scoring map and group completed tests by class."""
    section_classes = [name for _, classes in SECTIONS.values() for name, _ in classes]
    if len(section_classes) != len(POINTS) or set(section_classes) != set(POINTS):
        raise ScoringError("Scored class inventory does not match POINTS")
    selected_classes = {name for name, _ in SECTIONS[marker][1]} if marker else set(section_classes)
    expected = {node for node in EXPECTED_INVENTORY if node.split("::")[1] in selected_classes}
    if set(report["verification"]["inventory"]) != expected:
        raise ScoringError("Selected test inventory does not match the scoring section")

    results: dict[str, ClassResult] = {}
    for test in report["tests"]:
        _, name, method = test["nodeid"].split("::", 2)
        result = results.setdefault(
            name, {"passed": 0, "total": 0, "failures": [], "first_failure": ""}
        )
        result["total"] += 1
        if test["outcome"] == "passed":
            result["passed"] += 1
        else:
            result["failures"].append(method)
            if len(result["failures"]) == 1:
                result["first_failure"] = str(test["call"].get("longrepr", ""))[:1200]
    if set(results) != selected_classes:
        raise ScoringError("Executed tests do not cover all scored classes")
    return results


def earned_points(class_name: str, result: ClassResult) -> int:
    return POINTS[class_name] if result["passed"] == result["total"] else 0


def print_score(results: dict[str, ClassResult], marker: str | None, earned: int) -> None:
    print()
    print(f"{'Test class':<40} {'Status':<14} {'Points':>7}")
    print("-" * 65)
    for section, (heading, classes) in SECTIONS.items():
        if marker and marker != section:
            continue
        print(f"\n{heading}")
        for name, label in classes:
            result = results[name]
            passed, total = result["passed"], result["total"]
            status = "PASS" if passed == total else f"FAIL ({passed}/{total})"
            print(f"  {label:<38} {status:<14} {earned_points(name, result):>3}/{POINTS[name]}")
    print()
    print("-" * 65)
    possible = sum(POINTS[name] for name in results)
    if marker:
        print(f"{'Section score':<40} {earned:>3}/{possible}")
    else:
        print(f"{'TOTAL SCORE (autograded)':<40} {earned:>3}/{possible}")
        weighted = weighted_autograded(earned, possible)
        print(f"{'Weighted (90% of grade)':<40} {weighted:>5}/{AUTOGRADED_WEIGHT}")
        print(f"Writeup graded separately ({WRITEUP_POINTS} raw pts, {WRITEUP_WEIGHT}% of grade).")
    print()


def write_gradescope_results(results: dict[str, ClassResult], output: Path, earned: int) -> None:
    tests = []
    for _, classes in SECTIONS.values():
        for name, label in classes:
            result = results[name]
            passed, total = result["passed"], result["total"]
            detail = f"All {passed} test(s) passed."
            if result["failures"]:
                failures = ", ".join(result["failures"][:5])
                detail = f"{passed}/{total} test(s) passed.\nFailing: {failures}"
                if result["first_failure"]:
                    detail += f"\n\n{result['first_failure']}"
            tests.append(
                {
                    "score": earned_points(name, result),
                    "max_score": POINTS[name],
                    "name": label,
                    "output": detail,
                    "visibility": "visible",
                }
            )

    possible = sum(POINTS.values())
    weighted = weighted_autograded(earned, possible)
    data = {
        "score": weighted,
        "output": (
            f"Raw autograded score: {earned}/{possible}\n"
            f"Scaled to {AUTOGRADED_WEIGHT}% of the grade: "
            f"{AUTOGRADED_WEIGHT} x ({earned}/{possible}) = {weighted}/{AUTOGRADED_WEIGHT}\n"
            f"(writeup graded separately, worth {WRITEUP_WEIGHT}% of the grade)"
        ),
        "tests": tests,
    }
    output.write_text(json.dumps(data, indent=2))
    print(f"Wrote {output}  (raw {earned}/{possible} -> {weighted}/{AUTOGRADED_WEIGHT})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Score HW03 or build the submission zip.")
    parser.add_argument("marker", nargs="?", choices=tuple(SECTIONS))
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--zip", action="store_true")
    modes.add_argument("--gradescope", type=Path, metavar="PATH")
    modes.add_argument("--verification-json", type=Path, metavar="PATH", help=argparse.SUPPRESS)
    args = parser.parse_args()
    output = args.gradescope or args.verification_json
    if args.marker and (args.zip or output):
        parser.error("A section can only be selected when printing a local score.")
    if args.zip:
        build_zip()
        return
    if output:
        output.unlink(missing_ok=True)

    try:
        report = run_verified_pytest(EXPECTED_INVENTORY, args.marker)
        results = class_results(report, args.marker)
    except ScoringError as exc:
        print(f"Scoring could not complete: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    earned = sum(earned_points(name, result) for name, result in results.items())
    if args.gradescope:
        write_gradescope_results(results, args.gradescope, earned)
    elif args.verification_json:
        possible = sum(POINTS.values())
        receipt = dict(
            report["verification"],
            raw_score=earned,
            raw_max=possible,
            weighted_score=weighted_autograded(earned, possible),
            classes=results,
        )
        args.verification_json.write_text(json.dumps(receipt, indent=2))
    else:
        print_score(results, args.marker, earned)


if __name__ == "__main__":
    main()
