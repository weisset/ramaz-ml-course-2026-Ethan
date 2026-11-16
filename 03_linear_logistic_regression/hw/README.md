# HW03 — Linear and Logistic Regression

Read `spec.pdf` for the assignment contract. Use the Intro to ML and Linear
and Logistic Regression lecture notes alongside it.

## Setup

Open `hw/` in your editor and run the commands below from that directory.
If you need to install `uv`, see `00_python_bootcamp/hw/README.md`.

```bash
uv sync --locked --python 3.11
uv run pytest
uv run python score.py
```

To focus on a section, run `uv run pytest -m methods`, `uv run pytest -m pipeline`,
or `uv run pytest -m experiments`. You can pass the same section name to
`uv run python score.py` for its point breakdown.

## Experiments

Once the regression models work, run the synthetic-data smoke test:

```bash
uv run python pipeline.py
```

After completing the helpers in `analysis.py`, run:

```bash
uv run python analysis.py
```

This writes `loss_curve.png` and `decision_boundary.png` and prints the
numbers you need for `writeup.md`. The first run needs internet access to
fetch California Housing. If the download fails, connect to the internet and
rerun the command. The tests use local data and can run without the download.

## Grading

| Section | Points |
| --- | ---: |
| Methods | 40 |
| Pipeline | 30 |
| Experiment helpers | 20 |
| Writeup | 10 |

A test class earns its points when every test in the class passes. The four
writeup questions are graded manually out of 13 raw points and scaled to 10.

## Files

| File | What to do |
| --- | --- |
| `regression.py` | Implement the model classes and sigmoid from `spec.pdf`. |
| `analysis.py` | Implement the five helpers above the provided experiment driver. |
| `writeup.md` | Answer all four questions using your results. |

Keep the provided `spec.pdf`, `test_regression.py`, `conftest.py`, `pipeline.py`,
`score.py`, `scoring.py`, `pyproject.toml`, `uv.lock`, and `.python-version` intact.

## Submission

```bash
uv run python score.py --zip
```

Rename `hw03_submission.zip` to `lastname_firstname_hw03.zip` and upload it to
the [HW03 submission folder](https://drive.google.com/drive/folders/1sklVTDo35htGF_R8_zUlXDBH4DqCdNun).
The zip contains `regression.py`, `analysis.py`, and `writeup.md`.
