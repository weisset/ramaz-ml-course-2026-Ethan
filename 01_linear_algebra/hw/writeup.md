# HW01 Writeup — Matrices as Transformations

Finish Part 3, then run `uv run --frozen --python 3.11 python analysis.py` to generate `transforms.png`
and the printed values. Answer the three questions below using **your own**
figure and output. Replace each `[your answer here]` with your response.

---

## Question 1 (3 pts)

**What does each transformation change, and what does it preserve?**

Look at the rotation, scaling, and shear panels of your `transforms.png`.
For each of the three transformations, describe in a sentence or two:

- What changed about the arrow (size? angles? direction it points? proportions?).
- What stayed the same.

The rotation transformation changed the direction of the arrow and the angle to the x-axis, but the size and proportions stayed the same.

The scaling transformation changed the size and proportions, but the direction of the arrow and the angle to the x-axis stayed the same.

The shear transformation changed the size, proportions, and direction the arrow points, but the angle to the x-axis stayed the same.

---

## Question 2 (3 pts)

**Why are the R @ S and S @ R panels different?**

Both panels apply the *same* two matrices — a $60^\circ$ rotation and a
$(2, 0.5)$ scaling — to the *same* arrow, just in opposite order. Using your
figure and the printed matrices and arrow-tip positions:

- Describe how the two results differ.
- Explain *why* the order changes the outcome. Connect your explanation to the
  principle that $AB \neq BA$ in general. (Hint: in each
  composition, which transformation does the arrow experience first?)

The differences are: R @ S has a greater magnitude (and components) than S @ R; R @ S appears "straight" while S @ R has awkward proportions.

The order changes the outcome because the rotation transformation will change the positions of specific values, so if x is affected by row 1 in the scaling matrix, and only then rotated, a rotation first would mean that the value x is being transformed by a different row in the scaling matrix, because the scaling isn't uniform.

---

## Question 3 (4 pts)

**What does the matrix part of a dense neural-network layer do?**

A dense layer uses a weight matrix to transform its input vectors. Here,
consider only that matrix operation, before adding a bias or applying a
nonlinearity. Your Part 3 figure shows several $2 \times 2$ examples.

Using your own figure and printed output, explain:

- Choose one panel and describe what its matrix did geometrically. If $X$
  stores $N$ two-dimensional points as rows and the weight matrix $W$ has
  shape $(2, 2)$, what shape should the transformed points have? Explain how
  storing points in rows fits the lecture's column-vector expression $Wp$.
- Why can changing the order of two weight matrices change the output?
  Support your answer with your two arrow-tip positions from Question 2,
  identifying which transformation acts first in each composition.

[your answer here]
