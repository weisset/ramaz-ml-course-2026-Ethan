# HW02 — Derivatives and Autograd

**Prerequisites:** HW01 (comfortable with PyTorch tensors) and the Calculus &
Gradient Descent lecture (power rule, chain rule, partial derivatives, the
gradient, gradient descent update rule).

This assignment has two deliverables:

1. **Coding (this folder, 100 pts):** implement three derivative computations
   by hand in pure Python, implement the same three with `torch.autograd`,
   verify they agree, and answer the writeup questions.
2. **[Problem set](exercises/02_math_exercises.pdf) (take-home, 40 pts):** hand-computed derivatives, partial
   derivatives, gradient descent by hand, and a backprop mini-problem. Worked
   at home, then scanned/photographed and turned in digitally (see Submission
   below).

---

## Submission

**Coding:** run this from the `hw/` directory:

```bash
uv run --frozen --python 3.11 python score.py --zip
```

It creates `hw02_submission.zip` with exactly the right files inside
(`derivatives.py` and `writeup.md`). Rename it to
`lastname_firstname_hw02.zip` and upload it to the
[HW02 submission folder](https://drive.google.com/drive/folders/1BHiOI2-iPBxCMG5mopC9xH1LyM7nDzYr).

**Problem set:** scan or photograph your work, combine it into one PDF named
`lastname_firstname_hw02_problemset.pdf`, and upload it to the same
[HW02 submission folder](https://drive.google.com/drive/folders/1BHiOI2-iPBxCMG5mopC9xH1LyM7nDzYr)
as your coding zip — do not put it in the zip itself, upload it separately.

---

## Setup

Open this folder in your editor. Uses the pinned Python 3.11 and `uv` — see
`00_python_bootcamp/hw/README.md` for the one-time setup if you have not done it yet.

1. **Install dependencies:**
   ```bash
   uv sync --locked --python 3.11
   ```

2. **Run the tests to see where you stand:**
   ```bash
   uv run --frozen --python 3.11 pytest
   ```

3. **Check your score:**
   ```bash
   uv run --frozen --python 3.11 python score.py
   ```

4. **Score a specific part only:**
   ```bash
   uv run --frozen --python 3.11 python score.py manual     # Part 1 (manual derivatives)
   uv run --frozen --python 3.11 python score.py autograd   # Part 2 (autograd)
   ```

---

## Parts

### Part 1: Manual derivatives (`derivatives.py`) — 45 pts

Implement the three functions whose names start with `manual_`, using only
Python arithmetic — no `torch`, no `math` library. The tests enforce this.

| Function | Rule | Points |
|----------|------|--------|
| `manual_gradient_quadratic` | power rule on $f(x) = ax^2 + bx$ | 15 |
| `manual_gradient_composite` | chain rule on $f(x) = (x^3 + 2)^2$ | 15 |
| `manual_partial_gradients` | partials of $f(x,y) = x^2 + 3xy + 2y^2$ | 15 |

### Part 2: Autograd (`derivatives.py`) — 45 pts

Implement the three `autograd_*` functions. They compute the same derivatives
as Part 1 using `torch.autograd`, so the two halves cross-check each other.

| Function | Points |
|----------|--------|
| `autograd_gradient_quadratic` | 15 |
| `autograd_gradient_composite` | 15 |
| `autograd_partial_gradients` | 15 |

### Writeup (`writeup.md`) — 10 pts

When all six functions are done, print the manual-vs-autograd comparison
table:

```bash
uv run --frozen --python 3.11 python derivatives.py
```

Use the output to answer the three questions in `writeup.md`.

### Problem set (take-home) — 40 pts

Worked at home and graded by hand from your scanned/photographed submission
(see Submission above). Show all steps.

---

## Files

| File | What to do |
|------|------------|
| `derivatives.py` | Implement all six functions (the comparison script at the bottom is provided — leave it alone) |
| `writeup.md` | Answer the three questions using your own comparison-table output |

**Do not modify:** `test_derivatives.py`, `conftest.py`, `score.py`,
`pyproject.toml`, `uv.lock`, or
`scoring.py` (provided with the student package).

---

## Tips

- Do Part 1 first — the autograd tests compare against your manual results.
- **Test one function at a time:**
  ```bash
  uv run --frozen --python 3.11 pytest -k TestManualGradientComposite   # just the chain-rule tests
  uv run --frozen --python 3.11 pytest -k TestAutogradPartialGradients  # just the autograd partials
  ```
- The test failure messages show the expected value at each point — read them.
- Each docstring in `derivatives.py` states the exact function to
  differentiate and includes a worked example point.
- If manual and autograd disagree, check both the derivative rule and the
  function you built in PyTorch. Autograd differentiates the program you wrote;
  it cannot tell whether you encoded the intended function. Small floating-point
  differences are normal; the tests compare with a tolerance.

---

## Saving your work

Your files are saved on your own machine as you edit. **Commit and push your work to GitHub so
it is backed up and you can pick it up on another machine.**

You can do this entirely from the VS Code sidebar — no terminal needed:

1. Click the **Source Control** icon in the left sidebar (it looks like a branching tree)
2. Click **+** next to each changed file to stage it
3. Type a short commit message (e.g. `"complete part 1"`)
4. Click **Commit**, then **Sync Changes**

Your work is now saved to your GitHub fork. Get into the habit of doing this whenever
you finish a work session.
