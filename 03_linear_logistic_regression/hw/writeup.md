# HW03 Writeup — Linear and Logistic Regression

Run `uv run python analysis.py` to generate your results, then answer the
questions below. Replace each `[your answer here]` with your actual response.

---

## Question 1 (3 pts): Learning Rate Effects

**Run `analysis.py`. It trains your linear regression model with three learning
rates: `lr=2e-5`, `lr=0.02`, and `lr=1.0`. Look at the `loss_curve.png` plot
and the printed loss values.**

**a)** Describe what the loss curve looks like for each learning rate.
What happens to the loss over the 200 epochs in each case?

[your answer here]

**b)** Which learning rate worked best within these 200 epochs? Describe what
the other runs suggest about steps that are too small or too large. Use
specific numbers from your printed output to support your answer.

[your answer here]

---

## Question 2 (3 pts): The Decision Boundary

**Look at your `decision_boundary.png` and the printed learned parameters
`w = [w1, w2]` and `b`.**

**a)** The decision boundary is the line where $\hat{y} = 0.5$, which means
$\sigma(x_1 w_1 + x_2 w_2 + b) = 0.5$.
Since $\sigma(z) = 0.5$ exactly when $z = 0$, the boundary satisfies:

$$x_1 w_1 + x_2 w_2 + b = 0$$

Using your actual trained values of $w_1$, $w_2$, and $b$, rewrite this as a
line equation in the form $x_2 = m x_1 + c$.
What are $m$ and $c$ in terms of $w_1$, $w_2$, and $b$?
If $w_2 = 0$, describe the boundary directly from the equation instead.

[your answer here]

**b)** The plot shows the test points. How many of those points did the model
misclassify? Use the plot and the test accuracy to explain what you can conclude
about how well the model generalized to held-out examples.

[your answer here]

---

## Question 3 (4 pts): One Gradient, Two Models

**Your base class `LinearModel` has a single `gradient` method, yet it correctly
trains both `LinearRegression` and `LogisticRegression`. That works because both
gradients reduce to the exact same formula:**

$$\frac{\partial L}{\partial \mathbf{w}} = \frac{1}{n} X^\top (\hat{\mathbf{y}} - \mathbf{y})$$

**a)** Linear regression uses `MSE = (1/2n) sum (yhat_i - y_i)^2`. Differentiate
the squared error term $(\hat{y}_i - y_i)^2$ with respect to $w_j$ and show how
the factor of 2 from the power rule cancels the $1/2$ in front, leaving the
formula above. Where would an extra factor of 2 appear if you had **not**
included the $1/2$?

[your answer here]

**b)** Logistic regression uses binary cross-entropy with no $1/2$ factor, yet
its gradient is the *same* formula. Work through the BCE gradient yourself and explain in one or two sentences what
cancels in the BCE case so that no factor of 2 (and no leftover $\sigma'(z)$
term) survives.

[your answer here]

---

## Question 4 (3 pts): The Number You Have To Beat

**Before it trains the Iris model, `analysis.py` finds the most common class
in the training labels. The baseline always predicts that class and evaluates
those predictions on the test split.**

**a)** Report the baseline and model accuracies on the **test** split.
What is their difference in percentage points, and which scored higher?

[your answer here]

**b)** Why is a constant prediction a meaningful comparison? Consider another
dataset where class 0 is the training majority and accounts for 95 of the 100
test labels. If a model reported 94% test accuracy, what would you conclude
from comparing it with the baseline?

[your answer here]
