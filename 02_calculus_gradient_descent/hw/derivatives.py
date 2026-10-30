"""HW02 — Derivatives and Autograd

Part 1: Manual derivative implementations — translate the derivative rules
directly into Python arithmetic. No torch, no math library.

Part 2: Autograd implementations — use torch.autograd to compute the same
gradients automatically.

Lecture references: Computing Derivatives: The Rules; Partial Derivatives and
the Gradient; Computation Graphs and PyTorch Autograd. The comparison table is
teacher-provided analysis code.

Run tests:        uv run pytest
Check score:      uv run python score.py
Compare results:  uv run python derivatives.py
"""

from __future__ import annotations

import torch

# ── Part 1: Manual Derivatives ────────────────────────────────────────────────


def manual_gradient_quadratic(a: float, b: float, x_val: float) -> float:
    """Return d/dx of f(x) = a*x**2 + b*x evaluated at x = x_val.

    Compute this by hand using the power rule — no torch, no math library
    beyond basic arithmetic.

    Args:
        a: Coefficient of the x**2 term.
        b: Coefficient of the x term.
        x_val: The point at which to evaluate the derivative.

    Returns:
        The value of f'(x_val).

    Example:
        >>> manual_gradient_quadratic(1.0, 0.0, 2.0)
        4.0
        # f(x) = x**2  =>  f'(x) = 2x  =>  f'(2) = 4

    Hint:
        Apply the power rule to each term separately, then add.
        Recall: d/dx [c * x**n] = c * n * x**(n-1).
    """
    raise NotImplementedError("Implement manual_gradient_quadratic()")


def manual_gradient_composite(x_val: float) -> float:
    """Return d/dx of f(x) = (x**3 + 2)**2 evaluated at x = x_val.

    Compute this using the chain rule — no torch, no math library beyond
    basic arithmetic.

    Args:
        x_val: The point at which to evaluate the derivative.

    Returns:
        The value of f'(x_val).

    Example:
        >>> manual_gradient_composite(1.0)
        18.0
        # f'(1) = 18

    Hint:
        f is one function applied to the result of another. Chain rule: the
        derivative of the outer function, evaluated at the inner one, times the
        derivative of the inner one. Decide for yourself where the inner
        function stops and the outer operation begins, then differentiate each
        with the power rule from the previous problem.
    """
    raise NotImplementedError("Implement manual_gradient_composite()")


def manual_partial_gradients(x_val: float, y_val: float) -> tuple[float, float]:
    """Return (df/dx, df/dy) of f(x, y) = x**2 + 3*x*y + 2*y**2 at (x_val, y_val).

    Compute both partial derivatives by hand — no torch, no math library.

    Args:
        x_val: x-coordinate of the evaluation point.
        y_val: y-coordinate of the evaluation point.

    Returns:
        A tuple (df_dx, df_dy) of the two partial derivative values.

    Example:
        >>> manual_partial_gradients(1.0, 2.0)
        (8.0, 11.0)
        # at (1, 2): df/dx = 8.0, df/dy = 11.0

    Hint:
        For df/dx: treat y as a constant and differentiate with respect to x.
        For df/dy: treat x as a constant and differentiate with respect to y.
    """
    raise NotImplementedError("Implement manual_partial_gradients()")


# ── Part 2: Autograd ──────────────────────────────────────────────────────────


def autograd_gradient_quadratic(a: float, b: float, x_val: float) -> float:
    """Return d/dx of f(x) = a*x**2 + b*x at x = x_val using torch.autograd.

    Args:
        a: Coefficient of the x**2 term.
        b: Coefficient of the x term.
        x_val: The point at which to evaluate the derivative.

    Returns:
        The value of f'(x_val) as a plain Python float.

    Example:
        >>> autograd_gradient_quadratic(1.0, 0.0, 2.0)
        4.0

    Hint:
        PyTorch only tracks gradients for tensors you explicitly mark as
        needing them — find that flag. Build f from that tensor using ordinary
        arithmetic, then trigger the backward pass; the gradient is deposited
        on the input tensor, not returned. The return type must be a plain
        Python float, not a 0-dim tensor. See the autograd section of the
        lecture.
    """
    raise NotImplementedError("Implement autograd_gradient_quadratic()")


def autograd_gradient_composite(x_val: float) -> float:
    """Return d/dx of f(x) = (x**3 + 2)**2 at x = x_val using torch.autograd.

    Args:
        x_val: The point at which to evaluate the derivative.

    Returns:
        The value of f'(x_val) as a plain Python float.

    Example:
        >>> autograd_gradient_composite(1.0)
        18.0

    Hint:
        Same pattern as autograd_gradient_quadratic — just define f differently.
    """
    raise NotImplementedError("Implement autograd_gradient_composite()")


def autograd_partial_gradients(x_val: float, y_val: float) -> tuple[float, float]:
    """Return (df/dx, df/dy) of f(x, y) = x**2 + 3*x*y + 2*y**2 using torch.autograd.

    Args:
        x_val: x-coordinate of the evaluation point.
        y_val: y-coordinate of the evaluation point.

    Returns:
        A tuple (df_dx, df_dy) as plain Python floats.

    Example:
        >>> autograd_partial_gradients(1.0, 2.0)
        (8.0, 11.0)

    Hint:
        f depends on two inputs, but backward() is called once on a single
        scalar. Which tensors must be tracked, and where does each partial
        derivative end up?
    """
    raise NotImplementedError("Implement autograd_partial_gradients()")


# ── Comparison table (teacher-provided — do not modify) ───────────────────────
#
# Run with:  uv run python derivatives.py
#
# Evaluates each manual_* function and its autograd_* counterpart at several
# points and prints them side by side, so you can eyeball whether your two
# implementations agree. You will use this output in writeup.md.

_QUAD_POINTS: list[tuple[float, float, float]] = [
    (1.0, 0.0, 2.0),
    (3.0, 2.0, 1.0),
    (-2.0, 5.0, 1.0),
    (0.5, -1.0, 4.0),
]
_COMPOSITE_POINTS: list[float] = [0.0, 1.0, 2.0, -1.0]
_PARTIAL_POINTS: list[tuple[float, float]] = [
    (1.0, 2.0),
    (2.0, 1.0),
    (0.0, 0.0),
    (-1.0, 3.0),
]


def _print_row(label: str, manual_val: float, auto_val: float) -> None:
    diff = abs(manual_val - auto_val)
    print(f"{label:<44} {manual_val:>12.4f} {auto_val:>12.4f} {diff:>10.2e}")


if __name__ == "__main__":
    header = f"{'function @ point':<44} {'manual':>12} {'autograd':>12} {'|diff|':>10}"
    print(header)
    print("-" * len(header))

    for a, b, xv in _QUAD_POINTS:
        _print_row(
            f"quadratic   a={a:g}, b={b:g}, x={xv:g}",
            manual_gradient_quadratic(a, b, xv),
            autograd_gradient_quadratic(a, b, xv),
        )
    for xv in _COMPOSITE_POINTS:
        _print_row(
            f"composite   x={xv:g}",
            manual_gradient_composite(xv),
            autograd_gradient_composite(xv),
        )
    for xv, yv in _PARTIAL_POINTS:
        m_dx, m_dy = manual_partial_gradients(xv, yv)
        a_dx, a_dy = autograd_partial_gradients(xv, yv)
        _print_row(f"partial df/dx  (x,y)=({xv:g},{yv:g})", m_dx, a_dx)
        _print_row(f"partial df/dy  (x,y)=({xv:g},{yv:g})", m_dy, a_dy)

    print("-" * len(header))
    print("If every |diff| is ~0, your manual rules and autograd agree.")
