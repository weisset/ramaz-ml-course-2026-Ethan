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

function @ point                                   manual     autograd     |diff|
---------------------------------------------------------------------------------
quadratic   a=1, b=0, x=2                          4.0000       4.0000   0.00e+00
quadratic   a=3, b=2, x=1                          8.0000       8.0000   0.00e+00
quadratic   a=-2, b=5, x=1                         1.0000       1.0000   0.00e+00
quadratic   a=0.5, b=-1, x=4                       3.0000       3.0000   0.00e+00
composite   x=0                                    0.0000       0.0000   0.00e+00
composite   x=1                                   18.0000      18.0000   0.00e+00
composite   x=2                                  240.0000     240.0000   0.00e+00
composite   x=-1                                   6.0000       6.0000   0.00e+00
partial df/dx  (x,y)=(1,2)                         8.0000       8.0000   0.00e+00
partial df/dy  (x,y)=(1,2)                        11.0000      11.0000   0.00e+00
partial df/dx  (x,y)=(2,1)                         7.0000       7.0000   0.00e+00
partial df/dy  (x,y)=(2,1)                        10.0000      10.0000   0.00e+00
partial df/dx  (x,y)=(0,0)                         0.0000       0.0000   0.00e+00
partial df/dy  (x,y)=(0,0)                         0.0000       0.0000   0.00e+00
partial df/dx  (x,y)=(-1,3)                        7.0000       7.0000   0.00e+00
partial df/dy  (x,y)=(-1,3)                        9.0000       9.0000   0.00e+00
---------------------------------------------------------------------------------
If every |diff| is ~0, your manual rules and autograd agree.  
They all agree.

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

Outer (v): $v(u)=u^2$
Inner (u): $u(x)=x^3 + 2$

$v'(u)=2u$
$u'(x)=3x^2$

$f'(x)=v'(u(x)) \cdot u'(x)=2u(x) \cdot 3x^2 = (2x^3 + 4)3x^2 = 6x^5 + 12x^2$
It records that first step of cubing the input, then the adding 2 (those two are what i put for the inner function), then records that all of that gets squared. The backwards pass will return the derivative (which is the gradient since it's a single variable function) and store that function f', in the data for the tensor.
The steps of the backwards pass would be to do derivative with respect to the outer square, then multiplied by derivative with respect to the inner, which is going to be the derivative with respect to the cube plus derivative with respect to the constant, and then multiply that derivative with respect to the cubed by derivative with respect to x which is 1. that gets you 2(inner) * (1*3x^2 + 0) = 6x^2 * (inner)
 etc.
Then when we ask for .grad it applies that function to x which has whatever value we gave it and that is the gradient.

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

~**c) Choosing a method (1 pt).** Suppose you want the gradient of a scalar
function with $d$ inputs. Compare estimating each partial derivative using
forward differences with computing the gradient using PyTorch autograd:~

- ~How many function evaluations would forward differences require if you
  reuse the value at the original input? How does autograd avoid repeating
  that work separately for each input?~
- ~Which source of error does autograd avoid, and why are its results still
  not perfectly exact?~

~Refer to the lecture box **“Why not estimate derivatives from nearby values?”**
if needed.~

a. 
the value obtained is 18, and the new update would be x=1-0.01(18)=1-0.18=0.82. This would be a step to the left because we are decreasing the value of the parameter, since we are subtracting a scalar multiple of the gradient from the original value(s) of the parameter (the negative gradient is the steepest local **descent**).

b. so g+2 is 20, the new update would be 1-0.2 = 0.8, the difference between the old and new update are 0.02 (that is old - new). The direction would not change because the sign stays the same, but the distance would be greater. Since it keeps the direction, it's possible that increasing teh value of the gradient by a scalar constant could bring me even closer to a minimum loss, but i could also accidentally overshoot, but either way I will be going in the right direction (unless of course I cause the sign to switch).