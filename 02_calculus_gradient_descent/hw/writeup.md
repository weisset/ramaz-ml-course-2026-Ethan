# HW02 Writeup — Derivatives and Autograd

After implementing all six functions, run the comparison script:

```bash
uv run --frozen --python 3.11 python derivatives.py
```

It prints a side-by-side table of your manual gradients and your autograd
gradients. Use that output to answer the three questions below. Replace each
`[your answer here]` with your response.

---

## Question 1 (3 pts)

**Do your manual and autograd gradients agree?**

Paste (or neatly transcribe) the comparison table printed by
`uv run --frozen --python 3.11 python derivatives.py`. Then answer:

- Do the manual and autograd values agree, allowing for floating-point
  rounding, at **every** point in the table?
- If any pair disagreed at some point while you were developing your
  solutions, what was the bug, and how did the table (or the tests) help you
  find it? If they agreed on your first try, say so — and describe one
  specific mistake the table *would* have caught (for example, in which rows
  the numbers would split apart if you forgot part of a derivative rule).

[your answer here]

---

## Question 2 (4 pts)

**The chain rule, by hand and by `.backward()`.**

Take the composite function from this assignment, $f(x) = (x^3 + 2)^2$.

**a)** Write out the chain-rule steps you used in
`manual_gradient_composite`: identify the outer function and the inner
function, give the derivative of each, and show how they combine into
$f'(x)$.

**b)** Now explain what PyTorch is doing when `autograd_gradient_composite`
runs its backward pass. Autograd is bookkeeping of the
chain rule over a computation graph — walk through how *your* steps from
part (a) show up in that process: what operations get recorded as you build
`f` from the input, and how the backward pass combines their derivatives to
produce the gradient stored on your input tensor.

[your answer here]

---

## Question 3 (3 pts)

**From your gradient to a parameter update.**

**a) One update (1 pt).** Use the row for the composite function at $x=1$
from **your** comparison table. State the gradient value $g$ you obtained,
then compute one update $x_{new}=1-0.01g$. Explain why your step moves left
or right.

**b) A gradient error (1 pt).** Suppose the gradient used in that same step
were $g+2$ instead. Compute the new update and its difference from part (a).
Does this error change the direction, the distance, or both? A different
step is not automatically worse; explain what you can conclude from this
calculation without running further steps.

**c) Choosing a method (1 pt).** Suppose you want the gradient of a scalar
function with $d$ inputs. Compare estimating each partial derivative using
forward differences with computing the gradient using PyTorch autograd:

- How many function evaluations would forward differences require if you
  reuse the value at the original input? How does autograd avoid repeating
  that work separately for each input?
- Which source of error does autograd avoid, and why are its results still
  not perfectly exact?

Refer to the lecture box **“Why not estimate derivatives from nearby values?”**
if needed.

[your answer here]
