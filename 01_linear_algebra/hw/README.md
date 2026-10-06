# HW01 — Linear Algebra

**Prerequisites:** Python basics from HW00 and the Linear Algebra lecture notes
(vectors, matrices, dot products, matrix multiplication, matrices as transformations).

You will implement the core linear algebra operations twice — first from scratch in
pure Python, then as PyTorch one-liners — and then use 2x2 matrices to rotate, scale,
and shear a shape, seeing for yourself what "a matrix transforms space" means.

This assignment has two deliverables:

1. **Coding (this folder, 100 pts):** implement the operations above and answer the
   writeup questions.
2. **[Problem set](exercises/01_linear_algebra_exercises.pdf) (take-home, 40 pts):** hand-worked vector/matrix
   problems, scanned and turned in digitally (see Submission below).

---

## Submission

**Coding:** run this from the `hw/` directory:

```bash
uv run --frozen --python 3.11 python score.py --zip
```

It creates `hw01_submission.zip` with exactly the right files inside.
Rename it to `lastname_firstname_hw01.zip` and upload it to the
[HW01 submission folder](https://drive.google.com/drive/folders/19_iMdJl3vkrGuFP4qj-dpZXwFoUMv0gf).

**Problem set:** scan or photograph your work, combine it into one PDF named
`lastname_firstname_hw01_problemset.pdf`, and upload it to the same
[HW01 submission folder](https://drive.google.com/drive/folders/19_iMdJl3vkrGuFP4qj-dpZXwFoUMv0gf)
as your coding zip — do not put it in the zip itself, upload it separately.

---

## Setup

Open this folder in your editor. This assignment pins Python 3.11 and its
dependencies in `.python-version` and `uv.lock`. You need `uv` — see
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
   uv run --frozen --python 3.11 python score.py purepython    # Part 1
   uv run --frozen --python 3.11 python score.py torch         # Part 2
   uv run --frozen --python 3.11 python score.py transforms    # Part 3
   ```

---

## Parts

| Part | What you implement | Points |
|------|--------------------|--------|
| 1. Pure Python (`linear_algebra.py`) | 9 vector/matrix functions using only built-ins + `math` | 35 |
| 2. PyTorch mirrors (`linear_algebra.py`) | 6 of the same operations as PyTorch one-liners | 18 |
| 2b. Harder problems (`linear_algebra.py`) | `cosine_similarity`, `row_normalize`, `pairwise_distances` | 17 |
| 3. Transformations (`analysis.py`) | `rotation_matrix`, `scaling_matrix`, `shear_matrix`, `apply_transform` | 20 |
| Writeup (`writeup.md`) | 3 questions about your `transforms.png` | 10 |

### Part 1: Pure Python — no torch, no numpy

Vectors are `list[float]`; matrices are `list[list[float]]` (row-major). The tests
check that no Part 1 function uses torch — implement them with loops, comprehensions,
and the `math` module. Read each docstring: it tells you exactly what to implement
and shows examples.

### Part 2: PyTorch mirrors

The *same* operations, each in 1-3 lines using tensor operations from the lecture
examples (`torch.dot`, `@`, transpose, `torch.linalg.norm`). The point: PyTorch
does exactly the math you just wrote by hand, faster.

### Part 2b: Harder problems

Three functions that combine vector and matrix operations: `cosine_similarity`
compares two vectors (as embeddings are compared in Module 6), `row_normalize`
normalizes each matrix row, and `pairwise_distances` compares all pairs of rows. These take real thought.
A loop-based solution earns full credit; once it passes, try the vectorized
version — the docstring hints point the way. Shortcut functions that do the
whole job (`torch.cdist`, `torch.nn.functional.cosine_similarity`,
`torch.nn.functional.normalize`) are blocked.

### Part 3: Transformations (`analysis.py` + `writeup.md`)

Implement the four matrix-builder/apply functions, then run:

```bash
uv run --frozen --python 3.11 python analysis.py
```

It saves `transforms.png` (your shape rotated, scaled, sheared, and composed both
ways) and prints values. Use them to answer the three questions in `writeup.md`.

---

## Files

| File | What to do |
|------|------------|
| `linear_algebra.py` | Implement Parts 1 and 2 (replace each `raise NotImplementedError`) |
| `analysis.py` | Implement the four transformation functions (the plotting block at the bottom is provided — don't touch it) |
| `writeup.md` | Answer the three questions in full sentences |

**Do not modify:** `test_linear_algebra.py`, `test_analysis.py`, `conftest.py`,
`score.py`, `scoring.py`, `pyproject.toml`, `uv.lock`, or `.python-version`.
The function signatures and docstrings in the implementation files are the coding
contract; HW01 has no separate coding spec PDF.

---

## Tips

- Work in order — Part 1 functions build on each other (e.g., `matrix_multiply` can
  reuse `dot_product` and `matrix_transpose`), and Part 2 reuses Part 1's ideas.
- **Test one function at a time:**
  ```bash
  uv run --frozen --python 3.11 pytest -k TestDotProduct        # just the dot_product tests
  uv run --frozen --python 3.11 pytest -k TestRotationMatrix    # just the rotation_matrix tests
  ```
- The test failure messages are designed to tell you exactly what went wrong — read them.
- For Part 2 and Part 3, the lecture's PyTorch examples have every operation you need.
- `rotation_matrix` takes **degrees**; `math.cos`/`math.sin` take **radians**.

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
