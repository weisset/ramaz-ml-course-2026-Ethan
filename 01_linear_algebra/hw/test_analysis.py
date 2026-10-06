"""Tests for HW01 — analysis.py (Part 3: transformations)

Each class tests one function. All tests in a class must pass to earn credit.
Run with: uv run pytest -m transforms
"""

from __future__ import annotations

import math

import pytest
import torch

from analysis import apply_transform, rotation_matrix, scaling_matrix, shear_matrix


@pytest.mark.transforms
class TestRotationMatrix:
    def test_shape(self) -> None:
        result = rotation_matrix(30.0)
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )
        assert result.shape == (2, 2), (
            f"rotation_matrix should return a (2,2) tensor; got shape {tuple(result.shape)}"
        )

    def test_zero_degrees_is_identity(self) -> None:
        result = rotation_matrix(0.0)
        assert torch.allclose(result, torch.eye(2), atol=1e-5), (
            f"rotation_matrix(0) should be the identity matrix; got {result}"
        )

    def test_ninety_degrees(self) -> None:
        result = rotation_matrix(90.0)
        expected = torch.tensor([[0.0, -1.0], [1.0, 0.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"rotation_matrix(90) should be [[0,-1],[1,0]]; got {result}"
        )

    def test_sixty_degrees(self) -> None:
        result = rotation_matrix(60.0)
        c, s = math.cos(math.radians(60.0)), math.sin(math.radians(60.0))
        expected = torch.tensor([[c, -s], [s, c]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"rotation_matrix(60) should be [[cos60,-sin60],[sin60,cos60]] = {expected}; "
            f"got {result}. Did you convert degrees to radians?"
        )

    def test_one_eighty_degrees(self) -> None:
        result = rotation_matrix(180.0)
        expected = -torch.eye(2)
        assert torch.allclose(result, expected, atol=1e-5), (
            f"rotation_matrix(180) should be [[-1,0],[0,-1]]; got {result}"
        )


@pytest.mark.transforms
class TestScalingMatrix:
    def test_shape(self) -> None:
        result = scaling_matrix(2.0, 3.0)
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )
        assert result.shape == (2, 2), (
            f"scaling_matrix should return a (2,2) tensor; got shape {tuple(result.shape)}"
        )

    def test_basic(self) -> None:
        result = scaling_matrix(2.0, 3.0)
        expected = torch.tensor([[2.0, 0.0], [0.0, 3.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"scaling_matrix(2, 3) should be [[2,0],[0,3]]; got {result}"
        )

    def test_unit_scaling_is_identity(self) -> None:
        result = scaling_matrix(1.0, 1.0)
        assert torch.allclose(result, torch.eye(2), atol=1e-5), (
            f"scaling_matrix(1, 1) should be the identity matrix; got {result}"
        )

    def test_reflection(self) -> None:
        result = scaling_matrix(1.0, -1.0)
        expected = torch.tensor([[1.0, 0.0], [0.0, -1.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"scaling_matrix(1, -1) (reflection across the x-axis) should be "
            f"[[1,0],[0,-1]]; got {result}"
        )


@pytest.mark.transforms
class TestShearMatrix:
    def test_shape(self) -> None:
        result = shear_matrix(0.8)
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )
        assert result.shape == (2, 2), (
            f"shear_matrix should return a (2,2) tensor; got shape {tuple(result.shape)}"
        )

    def test_basic(self) -> None:
        result = shear_matrix(0.8)
        expected = torch.tensor([[1.0, 0.8], [0.0, 1.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"shear_matrix(0.8) should be [[1,0.8],[0,1]]; got {result}"
        )

    def test_zero_shear_is_identity(self) -> None:
        result = shear_matrix(0.0)
        assert torch.allclose(result, torch.eye(2), atol=1e-5), (
            f"shear_matrix(0) should be the identity matrix; got {result}"
        )

    def test_shifts_top_not_bottom(self) -> None:
        # A horizontal shear moves (x, y) to (x + k*y, y):
        # points on the x-axis (y=0) stay put; higher points slide right.
        H = shear_matrix(2.0)
        bottom = H @ torch.tensor([1.0, 0.0])
        top = H @ torch.tensor([1.0, 1.0])
        assert torch.allclose(bottom, torch.tensor([1.0, 0.0]), atol=1e-5), (
            f"Shear should leave points on the x-axis unchanged; (1,0) moved to {bottom}"
        )
        assert torch.allclose(top, torch.tensor([3.0, 1.0]), atol=1e-5), (
            f"shear_matrix(2) should move (1,1) to (1 + 2*1, 1) = (3,1); got {top}"
        )


@pytest.mark.transforms
class TestApplyTransform:
    def test_shape_preserved(self) -> None:
        points = torch.randn(7, 2)
        result = apply_transform(points, torch.eye(2))
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )
        assert result.shape == (7, 2), (
            f"apply_transform on (7,2) points should return shape (7,2); got {tuple(result.shape)}"
        )

    def test_identity_returns_same_points(self) -> None:
        points = torch.tensor([[1.0, 2.0], [3.0, -4.0], [0.0, 0.5]])
        result = apply_transform(points, torch.eye(2))
        assert torch.allclose(result, points, atol=1e-5), (
            f"Applying the identity matrix should leave every point unchanged; got {result}"
        )

    def test_ninety_degree_rotation(self) -> None:
        # 90-degree rotation sends (1,0) -> (0,1) and (0,1) -> (-1,0).
        points = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
        R90 = torch.tensor([[0.0, -1.0], [1.0, 0.0]])
        result = apply_transform(points, R90)
        expected = torch.tensor([[0.0, 1.0], [-1.0, 0.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"Rotating [[1,0],[0,1]] by 90 degrees should give [[0,1],[-1,0]]; got {result}"
        )

    def test_scaling(self) -> None:
        points = torch.tensor([[1.0, 1.0], [2.0, -3.0]])
        S = torch.tensor([[2.0, 0.0], [0.0, 0.5]])
        result = apply_transform(points, S)
        expected = torch.tensor([[2.0, 0.5], [4.0, -1.5]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"Scaling by (2, 0.5) should give [[2,0.5],[4,-1.5]]; got {result}"
        )

    def test_each_row_is_matrix_times_point(self) -> None:
        points = torch.tensor([[1.0, 2.0], [-0.5, 3.0], [4.0, 0.0]])
        M = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        result = apply_transform(points, M)
        for i in range(points.shape[0]):
            expected_i = M @ points[i]
            assert torch.allclose(result[i], expected_i, atol=1e-5), (
                f"Row {i}: expected M @ point = {expected_i.tolist()}; "
                f"got {result[i].tolist()}. Each output row should be the matrix "
                "applied to the corresponding input point."
            )
