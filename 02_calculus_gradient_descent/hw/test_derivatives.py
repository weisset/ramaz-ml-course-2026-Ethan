"""Tests for HW02 — derivatives.py

Each class tests one function. All tests in a class must pass to earn credit.
Run with: uv run pytest
"""

from __future__ import annotations

import pytest

from derivatives import (
    autograd_gradient_composite,
    autograd_gradient_quadratic,
    autograd_partial_gradients,
    manual_gradient_composite,
    manual_gradient_quadratic,
    manual_partial_gradients,
)

TOL = 1e-4

# ── Part 1: Manual Derivatives ────────────────────────────────────────────────


@pytest.mark.manual
class TestManualGradientQuadratic:
    """d/dx of f(x) = a*x**2 + b*x — implemented by hand."""

    def test_pure_quadratic(self) -> None:
        result = manual_gradient_quadratic(1.0, 0.0, 2.0)
        assert abs(result - 4.0) < TOL, (
            f"manual_gradient_quadratic(1, 0, 2) should be 4.0, got {result}"
        )

    def test_with_linear_term(self) -> None:
        result = manual_gradient_quadratic(3.0, 2.0, 1.0)
        assert abs(result - 8.0) < TOL, (
            f"manual_gradient_quadratic(3, 2, 1) should be 8.0, got {result}"
        )

    def test_negative_coefficients(self) -> None:
        result = manual_gradient_quadratic(-2.0, 5.0, 1.0)
        assert abs(result - 1.0) < TOL, (
            f"manual_gradient_quadratic(-2, 5, 1) should be 1.0, got {result}"
        )

    def test_at_zero(self) -> None:
        result = manual_gradient_quadratic(4.0, -3.0, 0.0)
        assert abs(result - (-3.0)) < TOL, (
            f"manual_gradient_quadratic(4, -3, 0) should be -3.0, got {result}"
        )

    def test_fractional_coefficients(self) -> None:
        result = manual_gradient_quadratic(0.5, -1.0, 4.0)
        assert abs(result - 3.0) < TOL, (
            f"manual_gradient_quadratic(0.5, -1, 4) should be 3.0, got {result}"
        )


@pytest.mark.manual
class TestManualGradientComposite:
    """d/dx of f(x) = (x**3 + 2)**2 — chain rule applied by hand."""

    def test_at_one(self) -> None:
        result = manual_gradient_composite(1.0)
        assert abs(result - 18.0) < TOL, (
            f"manual_gradient_composite(1) should be 18.0, got {result} "
            f"(a common bug is dropping the inner derivative factor)"
        )

    def test_at_zero(self) -> None:
        result = manual_gradient_composite(0.0)
        assert abs(result - 0.0) < TOL, f"manual_gradient_composite(0) should be 0.0, got {result}"

    def test_at_two(self) -> None:
        result = manual_gradient_composite(2.0)
        assert abs(result - 240.0) < TOL, (
            f"manual_gradient_composite(2) should be 240.0, got {result}"
        )

    def test_negative_input(self) -> None:
        result = manual_gradient_composite(-1.0)
        assert abs(result - 6.0) < TOL, f"manual_gradient_composite(-1) should be 6.0, got {result}"


@pytest.mark.manual
class TestManualPartialGradients:
    """(df/dx, df/dy) of f(x,y) = x**2 + 3xy + 2y**2 — both partials by hand."""

    def test_basic_point(self) -> None:
        dx, dy = manual_partial_gradients(1.0, 2.0)
        assert abs(dx - 8.0) < TOL, f"df/dx at (1,2) should be 8.0, got {dx}"
        assert abs(dy - 11.0) < TOL, f"df/dy at (1,2) should be 11.0, got {dy}"

    def test_at_origin(self) -> None:
        dx, dy = manual_partial_gradients(0.0, 0.0)
        assert abs(dx - 0.0) < TOL, f"df/dx at (0,0) should be 0.0, got {dx}"
        assert abs(dy - 0.0) < TOL, f"df/dy at (0,0) should be 0.0, got {dy}"

    def test_asymmetric_point(self) -> None:
        dx, dy = manual_partial_gradients(2.0, 1.0)
        assert abs(dx - 7.0) < TOL, f"df/dx at (2,1) should be 7.0, got {dx}"
        assert abs(dy - 10.0) < TOL, f"df/dy at (2,1) should be 10.0, got {dy}"

    def test_returns_tuple(self) -> None:
        result = manual_partial_gradients(1.0, 1.0)
        assert isinstance(result, tuple) and len(result) == 2, (
            f"manual_partial_gradients should return a tuple of length 2, got {type(result)}"
        )


# ── Part 2: Autograd ──────────────────────────────────────────────────────────


@pytest.mark.autograd
class TestAutogradGradientQuadratic:
    """Autograd version of the quadratic gradient — must match Part 1 results."""

    def test_matches_manual(self) -> None:
        manual = manual_gradient_quadratic(1.0, 0.0, 2.0)
        auto = autograd_gradient_quadratic(1.0, 0.0, 2.0)
        assert abs(auto - manual) < TOL, (
            f"autograd_gradient_quadratic(1, 0, 2) should match manual result {manual}, got {auto}"
        )

    def test_with_linear_term(self) -> None:
        auto = autograd_gradient_quadratic(3.0, 2.0, 1.0)
        assert abs(auto - 8.0) < TOL, (
            f"autograd_gradient_quadratic(3, 2, 1) should be 8.0, got {auto}"
        )

    def test_negative_coefficients(self) -> None:
        auto = autograd_gradient_quadratic(-2.0, 5.0, 1.0)
        assert abs(auto - 1.0) < TOL, (
            f"autograd_gradient_quadratic(-2, 5, 1) should be 1.0, got {auto}"
        )

    def test_returns_float(self) -> None:
        result = autograd_gradient_quadratic(1.0, 0.0, 1.0)
        assert isinstance(result, float), (
            f"autograd_gradient_quadratic should return a Python float, "
            f"got {type(result).__name__}. Use .item() to convert from a tensor."
        )


@pytest.mark.autograd
class TestAutogradGradientComposite:
    """Autograd version of the composite gradient — must match Part 1 results."""

    def test_matches_manual(self) -> None:
        manual = manual_gradient_composite(1.0)
        auto = autograd_gradient_composite(1.0)
        assert abs(auto - manual) < TOL, (
            f"autograd_gradient_composite(1) should match manual result {manual}, got {auto}"
        )

    def test_at_zero(self) -> None:
        auto = autograd_gradient_composite(0.0)
        assert abs(auto - 0.0) < TOL, f"autograd_gradient_composite(0) should be 0.0, got {auto}"

    def test_at_two(self) -> None:
        auto = autograd_gradient_composite(2.0)
        assert abs(auto - 240.0) < TOL, (
            f"autograd_gradient_composite(2) should be 240.0, got {auto}"
        )

    def test_returns_float(self) -> None:
        result = autograd_gradient_composite(1.0)
        assert isinstance(result, float), (
            f"autograd_gradient_composite should return a Python float, "
            f"got {type(result).__name__}. Use .item() to convert from a tensor."
        )


@pytest.mark.autograd
class TestAutogradPartialGradients:
    """Autograd partial gradients — must match Part 1 results."""

    def test_matches_manual(self) -> None:
        m_dx, m_dy = manual_partial_gradients(1.0, 2.0)
        a_dx, a_dy = autograd_partial_gradients(1.0, 2.0)
        assert abs(a_dx - m_dx) < TOL, (
            f"autograd df/dx at (1,2) should match manual {m_dx}, got {a_dx}"
        )
        assert abs(a_dy - m_dy) < TOL, (
            f"autograd df/dy at (1,2) should match manual {m_dy}, got {a_dy}"
        )

    def test_at_origin(self) -> None:
        a_dx, a_dy = autograd_partial_gradients(0.0, 0.0)
        assert abs(a_dx - 0.0) < TOL, f"autograd df/dx at (0,0) should be 0.0, got {a_dx}"
        assert abs(a_dy - 0.0) < TOL, f"autograd df/dy at (0,0) should be 0.0, got {a_dy}"

    def test_asymmetric_point(self) -> None:
        a_dx, a_dy = autograd_partial_gradients(2.0, 1.0)
        assert abs(a_dx - 7.0) < TOL, f"autograd df/dx at (2,1) should be 7.0, got {a_dx}"
        assert abs(a_dy - 10.0) < TOL, f"autograd df/dy at (2,1) should be 10.0, got {a_dy}"

    def test_returns_tuple_of_floats(self) -> None:
        result = autograd_partial_gradients(1.0, 1.0)
        assert isinstance(result, tuple) and len(result) == 2, (
            f"autograd_partial_gradients should return a tuple of length 2, got {type(result)}"
        )
        dx, dy = result
        assert isinstance(dx, float) and isinstance(dy, float), (
            f"Both elements should be Python floats (use .item()), "
            f"got {type(dx).__name__} and {type(dy).__name__}"
        )
