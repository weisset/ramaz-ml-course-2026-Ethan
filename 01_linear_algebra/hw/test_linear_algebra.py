"""Tests for HW01 — linear_algebra.py (Parts 1 and 2)

Each class tests one function. All tests in a class must pass to earn credit.
Run with: uv run pytest
"""

from __future__ import annotations

import pytest
import torch

from linear_algebra import (
    cosine_similarity,
    dot_product,
    dot_product_torch,
    matrix_add,
    matrix_multiply,
    matrix_multiply_torch,
    matrix_transpose,
    matrix_transpose_torch,
    matrix_vector_multiply,
    matrix_vector_multiply_torch,
    normalize_vector,
    normalize_vector_torch,
    pairwise_distances,
    row_normalize,
    scalar_multiply,
    vector_add,
    vector_magnitude,
    vector_magnitude_torch,
)

# ── Part 1: From Scratch ──────────────────────────────────────────────────────


@pytest.mark.purepython
class TestVectorAdd:
    def test_basic(self) -> None:
        result = vector_add([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
        assert result == [5.0, 7.0, 9.0], (
            f"vector_add([1,2,3], [4,5,6]) should return [5,7,9]; got {result}"
        )

    def test_negative_values(self) -> None:
        result = vector_add([-1.0, -2.0], [1.0, 2.0])
        assert result == [0.0, 0.0], f"vector_add([-1,-2], [1,2]) should return [0,0]; got {result}"

    def test_single_element(self) -> None:
        result = vector_add([7.0], [3.0])
        assert result == [10.0], f"vector_add([7], [3]) should return [10]; got {result}"

    def test_returns_list(self) -> None:
        result = vector_add([1.0, 2.0], [3.0, 4.0])
        assert isinstance(result, list), f"Return type should be list, not {type(result).__name__}"

    def test_floats(self) -> None:
        result = vector_add([0.1, 0.2], [0.3, 0.4])
        assert abs(result[0] - 0.4) < 1e-6, f"0.1 + 0.3 should be close to 0.4; got {result[0]}"
        assert abs(result[1] - 0.6) < 1e-6, f"0.2 + 0.4 should be close to 0.6; got {result[1]}"


@pytest.mark.purepython
class TestScalarMultiply:
    def test_basic(self) -> None:
        result = scalar_multiply(3.0, [1.0, 2.0, 3.0])
        assert result == [3.0, 6.0, 9.0], (
            f"scalar_multiply(3, [1,2,3]) should return [3,6,9]; got {result}"
        )

    def test_zero_scalar(self) -> None:
        result = scalar_multiply(0.0, [1.0, 2.0, 3.0])
        assert result == [0.0, 0.0, 0.0], (
            f"Multiplying by 0 should return the zero vector; got {result}"
        )

    def test_negative_scalar(self) -> None:
        result = scalar_multiply(-1.0, [1.0, -2.0, 3.0])
        assert result == [-1.0, 2.0, -3.0], (
            f"scalar_multiply(-1, [1,-2,3]) should return [-1,2,-3]; got {result}"
        )

    def test_returns_list(self) -> None:
        result = scalar_multiply(2.0, [1.0, 2.0])
        assert isinstance(result, list), f"Return type should be list, not {type(result).__name__}"

    def test_fractional_scalar(self) -> None:
        result = scalar_multiply(0.5, [4.0, 8.0])
        assert abs(result[0] - 2.0) < 1e-6, f"0.5 * 4.0 should be 2.0; got {result[0]}"
        assert abs(result[1] - 4.0) < 1e-6, f"0.5 * 8.0 should be 4.0; got {result[1]}"


@pytest.mark.purepython
class TestDotProduct:
    def test_basic(self) -> None:
        result = dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
        assert abs(result - 32.0) < 1e-6, f"dot([1,2,3], [4,5,6]) = 1*4+2*5+3*6 = 32; got {result}"

    def test_orthogonal_vectors(self) -> None:
        result = dot_product([1.0, 0.0], [0.0, 1.0])
        assert abs(result - 0.0) < 1e-6, f"Orthogonal unit vectors have dot product 0; got {result}"

    def test_parallel_unit_vectors(self) -> None:
        result = dot_product([1.0, 0.0], [1.0, 0.0])
        assert abs(result - 1.0) < 1e-6, f"Identical unit vectors have dot product 1; got {result}"

    def test_returns_float(self) -> None:
        result = dot_product([1.0, 2.0], [3.0, 4.0])
        assert isinstance(result, float), (
            f"Return type should be float, not {type(result).__name__}"
        )

    def test_negative_values(self) -> None:
        result = dot_product([-1.0, -2.0], [3.0, 4.0])
        assert abs(result - (-11.0)) < 1e-6, f"dot([-1,-2], [3,4]) = -3 + -8 = -11; got {result}"


@pytest.mark.purepython
class TestVectorMagnitude:
    def test_three_four_five(self) -> None:
        result = vector_magnitude([3.0, 4.0])
        assert abs(result - 5.0) < 1e-6, f"magnitude([3,4]) = sqrt(9+16) = 5; got {result}"

    def test_unit_vector(self) -> None:
        result = vector_magnitude([1.0, 0.0])
        assert abs(result - 1.0) < 1e-6, f"Unit vector [1,0] has magnitude 1; got {result}"

    def test_zero_vector(self) -> None:
        result = vector_magnitude([0.0, 0.0, 0.0])
        assert abs(result - 0.0) < 1e-6, f"Zero vector has magnitude 0; got {result}"

    def test_three_dimensions(self) -> None:
        result = vector_magnitude([1.0, 2.0, 2.0])
        assert abs(result - 3.0) < 1e-6, f"magnitude([1,2,2]) = sqrt(1+4+4) = 3; got {result}"

    def test_returns_float(self) -> None:
        result = vector_magnitude([3.0, 4.0])
        assert isinstance(result, float), (
            f"Return type should be float, not {type(result).__name__}"
        )


@pytest.mark.purepython
class TestNormalizeVector:
    def test_basic(self) -> None:
        result = normalize_vector([3.0, 4.0])
        assert abs(result[0] - 0.6) < 1e-6, f"normalize([3,4])[0] should be 0.6; got {result[0]}"
        assert abs(result[1] - 0.8) < 1e-6, f"normalize([3,4])[1] should be 0.8; got {result[1]}"

    def test_unit_vector_unchanged(self) -> None:
        result = normalize_vector([1.0, 0.0])
        assert abs(result[0] - 1.0) < 1e-6, (
            f"Normalizing a unit vector should leave it unchanged; got {result}"
        )
        assert abs(result[1] - 0.0) < 1e-6, (
            f"Normalizing a unit vector should leave it unchanged; got {result}"
        )

    def test_result_has_magnitude_one(self) -> None:
        result = normalize_vector([3.0, 4.0])
        mag = sum(x**2 for x in result) ** 0.5
        assert abs(mag - 1.0) < 1e-6, f"Normalized vector must have magnitude 1; got {mag}"

    def test_zero_vector_raises(self) -> None:
        with pytest.raises(ValueError):
            normalize_vector([0.0, 0.0, 0.0])

    def test_returns_list(self) -> None:
        result = normalize_vector([3.0, 4.0])
        assert isinstance(result, list), f"Return type should be list, not {type(result).__name__}"


@pytest.mark.purepython
class TestMatrixAdd:
    def test_basic(self) -> None:
        A = [[1.0, 2.0], [3.0, 4.0]]
        B = [[5.0, 6.0], [7.0, 8.0]]
        result = matrix_add(A, B)
        assert result == [[6.0, 8.0], [10.0, 12.0]], (
            f"matrix_add([[1,2],[3,4]], [[5,6],[7,8]]) should return [[6,8],[10,12]]; got {result}"
        )

    def test_zero_matrix(self) -> None:
        A = [[1.0, 2.0], [3.0, 4.0]]
        Z = [[0.0, 0.0], [0.0, 0.0]]
        result = matrix_add(A, Z)
        assert result == [[1.0, 2.0], [3.0, 4.0]], (
            f"Adding a zero matrix should return the original matrix; got {result}"
        )

    def test_negative_values(self) -> None:
        A = [[1.0, -2.0], [-3.0, 4.0]]
        B = [[-1.0, 2.0], [3.0, -4.0]]
        result = matrix_add(A, B)
        assert result == [[0.0, 0.0], [0.0, 0.0]], (
            f"Negatives cancel; expected [[0,0],[0,0]]; got {result}"
        )

    def test_returns_list_of_lists(self) -> None:
        result = matrix_add([[1.0]], [[2.0]])
        assert isinstance(result, list) and isinstance(result[0], list), (
            f"Return type should be list[list[float]]; got {type(result)}"
        )

    def test_three_by_three(self) -> None:
        A = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        B = [[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]
        result = matrix_add(A, B)
        assert result[0][1] == 1.0, f"result[0][1] should be 1.0; got {result[0][1]}"
        assert result[1][0] == 1.0, f"result[1][0] should be 1.0; got {result[1][0]}"


@pytest.mark.purepython
class TestMatrixVectorMultiply:
    def test_identity(self) -> None:
        identity = [[1.0, 0.0], [0.0, 1.0]]
        v = [3.0, 7.0]
        result = matrix_vector_multiply(identity, v)
        assert result == [3.0, 7.0], f"Identity matrix times v should return v; got {result}"

    def test_basic(self) -> None:
        A = [[1.0, 2.0], [3.0, 4.0]]
        v = [1.0, 1.0]
        result = matrix_vector_multiply(A, v)
        assert result == [3.0, 7.0], f"[[1,2],[3,4]] @ [1,1] = [1+2, 3+4] = [3,7]; got {result}"

    def test_two_by_three(self) -> None:
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        v = [1.0, 0.0, 1.0]
        result = matrix_vector_multiply(A, v)
        assert abs(result[0] - 4.0) < 1e-6, f"Row 0: 1*1+2*0+3*1 = 4; got {result[0]}"
        assert abs(result[1] - 10.0) < 1e-6, f"Row 1: 4*1+5*0+6*1 = 10; got {result[1]}"

    def test_output_length(self) -> None:
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
        v = [1.0, 2.0, 3.0]
        result = matrix_vector_multiply(A, v)
        assert len(result) == 3, (
            f"3x3 matrix times 3-vector should give 3-vector; got length {len(result)}"
        )

    def test_returns_list(self) -> None:
        result = matrix_vector_multiply([[1.0, 0.0]], [5.0, 3.0])
        assert isinstance(result, list), f"Return type should be list, not {type(result).__name__}"


@pytest.mark.purepython
class TestMatrixMultiply:
    def test_two_by_two(self) -> None:
        A = [[1.0, 2.0], [3.0, 4.0]]
        B = [[5.0, 6.0], [7.0, 8.0]]
        result = matrix_multiply(A, B)
        expected = [[19.0, 22.0], [43.0, 50.0]]
        assert result == expected, (
            f"[[1,2],[3,4]] @ [[5,6],[7,8]] = [[19,22],[43,50]]; got {result}"
        )

    def test_identity(self) -> None:
        identity = [[1.0, 0.0], [0.0, 1.0]]
        A = [[3.0, 7.0], [1.0, 5.0]]
        result = matrix_multiply(identity, A)
        assert result == A, f"Identity @ A should return A; got {result}"

    def test_non_square(self) -> None:
        # A is 2x3, B is 3x2 -> result is 2x2
        # Expected: [[58, 64], [139, 154]]
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        B = [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]
        result = matrix_multiply(A, B)
        expected = [[58.0, 64.0], [139.0, 154.0]]
        assert len(result) == 2, f"Result should have 2 rows; got {len(result)}"
        assert len(result[0]) == 2, f"Result should have 2 columns; got {len(result[0])}"
        for i in range(2):
            for j in range(2):
                assert abs(result[i][j] - expected[i][j]) < 1e-6, (
                    f"result[{i}][{j}] should be {expected[i][j]}; got {result[i][j]}"
                )

    def test_output_shape(self) -> None:
        # 3x2 times 2x4 -> 3x4
        A = [[float(i) for i in range(2)] for _ in range(3)]
        B = [[float(i) for i in range(4)] for _ in range(2)]
        result = matrix_multiply(A, B)
        assert len(result) == 3, f"Expected 3 rows; got {len(result)}"
        assert len(result[0]) == 4, f"Expected 4 cols; got {len(result[0])}"

    def test_returns_list_of_lists(self) -> None:
        result = matrix_multiply([[1.0]], [[2.0]])
        assert isinstance(result, list) and isinstance(result[0], list), (
            f"Return type should be list[list[float]]; got {type(result)}"
        )


@pytest.mark.purepython
class TestMatrixTranspose:
    def test_two_by_three(self) -> None:
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        result = matrix_transpose(A)
        expected = [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
        assert result == expected, f"Transpose of 2x3 matrix should be 3x2; got {result}"

    def test_square(self) -> None:
        A = [[1.0, 2.0], [3.0, 4.0]]
        result = matrix_transpose(A)
        assert result == [[1.0, 3.0], [2.0, 4.0]], (
            f"Transpose of [[1,2],[3,4]] = [[1,3],[2,4]]; got {result}"
        )

    def test_double_transpose_is_identity(self) -> None:
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        assert matrix_transpose(matrix_transpose(A)) == A, (
            "Transposing twice should give the original matrix"
        )

    def test_shape(self) -> None:
        A = [[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]
        result = matrix_transpose(A)
        assert len(result) == 4, f"Transposed 2x4 should have 4 rows; got {len(result)}"
        assert len(result[0]) == 2, f"Transposed 2x4 should have 2 cols; got {len(result[0])}"

    def test_returns_list_of_lists(self) -> None:
        result = matrix_transpose([[1.0, 2.0]])
        assert isinstance(result, list) and isinstance(result[0], list), (
            f"Return type should be list[list[float]]; got {type(result)}"
        )


# ── Part 2: PyTorch Mirrors ───────────────────────────────────────────────────


@pytest.mark.torch
class TestDotProductTorch:
    def test_basic(self) -> None:
        u = torch.tensor([1.0, 2.0, 3.0])
        v = torch.tensor([4.0, 5.0, 6.0])
        result = dot_product_torch(u, v)
        expected = torch.tensor(32.0)
        assert torch.allclose(result, expected, atol=1e-5), (
            f"dot_product_torch([1,2,3], [4,5,6]) = 1*4+2*5+3*6 = 32; got {result}"
        )

    def test_orthogonal_vectors(self) -> None:
        result = dot_product_torch(torch.tensor([1.0, 0.0]), torch.tensor([0.0, 1.0]))
        assert torch.allclose(result, torch.tensor(0.0), atol=1e-5), (
            f"Orthogonal unit vectors have dot product 0; got {result}"
        )

    def test_negative_values(self) -> None:
        result = dot_product_torch(torch.tensor([-1.0, -2.0]), torch.tensor([3.0, 4.0]))
        expected = torch.tensor(-11.0)
        assert torch.allclose(result, expected, atol=1e-5), (
            f"dot_product_torch([-1,-2], [3,4]) = -3 + -8 = -11; got {result}"
        )

    def test_returns_scalar_tensor(self) -> None:
        result = dot_product_torch(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 4.0]))
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )
        assert result.dim() == 0, (
            f"Result should be a 0-dimensional (scalar) tensor; got shape {tuple(result.shape)}"
        )


@pytest.mark.torch
class TestVectorMagnitudeTorch:
    def test_three_four_five(self) -> None:
        result = vector_magnitude_torch(torch.tensor([3.0, 4.0]))
        expected = torch.tensor(5.0)
        assert torch.allclose(result, expected, atol=1e-5), (
            f"vector_magnitude_torch([3,4]) = sqrt(9+16) = 5; got {result}"
        )

    def test_unit_vector(self) -> None:
        result = vector_magnitude_torch(torch.tensor([1.0, 0.0]))
        assert torch.allclose(result, torch.tensor(1.0), atol=1e-5), (
            f"Unit vector [1,0] has magnitude 1; got {result}"
        )

    def test_three_dimensions(self) -> None:
        result = vector_magnitude_torch(torch.tensor([1.0, 2.0, 2.0]))
        expected = torch.tensor(3.0)
        assert torch.allclose(result, expected, atol=1e-5), (
            f"vector_magnitude_torch([1,2,2]) = sqrt(1+4+4) = 3; got {result}"
        )

    def test_zero_vector(self) -> None:
        result = vector_magnitude_torch(torch.zeros(3))
        assert torch.allclose(result, torch.tensor(0.0), atol=1e-5), (
            f"Zero vector has magnitude 0; got {result}"
        )

    def test_returns_tensor(self) -> None:
        result = vector_magnitude_torch(torch.tensor([3.0, 4.0]))
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )


@pytest.mark.torch
class TestNormalizeVectorTorch:
    def test_basic(self) -> None:
        result = normalize_vector_torch(torch.tensor([3.0, 4.0]))
        expected = torch.tensor([0.6, 0.8])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"normalize_vector_torch([3,4]) should be [0.6, 0.8]; got {result}"
        )

    def test_result_has_magnitude_one(self) -> None:
        result = normalize_vector_torch(torch.tensor([1.0, 2.0, 2.0]))
        mag = torch.linalg.norm(result)
        assert torch.allclose(mag, torch.tensor(1.0), atol=1e-5), (
            f"Normalized vector must have magnitude 1; got {mag}"
        )

    def test_unit_vector_unchanged(self) -> None:
        v = torch.tensor([0.0, 1.0])
        result = normalize_vector_torch(v)
        assert torch.allclose(result, v, atol=1e-5), (
            f"Normalizing a unit vector should leave it unchanged; got {result}"
        )

    def test_zero_vector_raises(self) -> None:
        with pytest.raises(ValueError):
            normalize_vector_torch(torch.zeros(3))

    def test_returns_tensor(self) -> None:
        result = normalize_vector_torch(torch.tensor([3.0, 4.0]))
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )


@pytest.mark.torch
class TestMatrixVectorMultiplyTorch:
    def test_identity(self) -> None:
        result = matrix_vector_multiply_torch(torch.eye(2), torch.tensor([3.0, 7.0]))
        expected = torch.tensor([3.0, 7.0])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"Identity matrix times v should return v; got {result}"
        )

    def test_basic(self) -> None:
        A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        result = matrix_vector_multiply_torch(A, torch.tensor([1.0, 1.0]))
        expected = torch.tensor([3.0, 7.0])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"[[1,2],[3,4]] @ [1,1] = [1+2, 3+4] = [3,7]; got {result}"
        )

    def test_two_by_three(self) -> None:
        A = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        v = torch.tensor([1.0, 0.0, 1.0])
        result = matrix_vector_multiply_torch(A, v)
        expected = torch.tensor([4.0, 10.0])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"Row 0: 1*1+2*0+3*1 = 4; row 1: 4*1+5*0+6*1 = 10; got {result}"
        )

    def test_output_shape(self) -> None:
        A = torch.ones(3, 4)
        v = torch.ones(4)
        result = matrix_vector_multiply_torch(A, v)
        assert result.shape == (3,), (
            f"(3,4) matrix times length-4 vector should give shape (3,); got {tuple(result.shape)}"
        )

    def test_returns_tensor(self) -> None:
        result = matrix_vector_multiply_torch(torch.eye(2), torch.ones(2))
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )


@pytest.mark.torch
class TestMatrixMultiplyTorch:
    def test_two_by_two(self) -> None:
        A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        B = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
        result = matrix_multiply_torch(A, B)
        expected = torch.tensor([[19.0, 22.0], [43.0, 50.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"[[1,2],[3,4]] @ [[5,6],[7,8]] = [[19,22],[43,50]]; got {result}"
        )

    def test_identity(self) -> None:
        A = torch.tensor([[3.0, 7.0], [1.0, 5.0]])
        result = matrix_multiply_torch(torch.eye(2), A)
        assert torch.allclose(result, A, atol=1e-5), f"Identity @ A should return A; got {result}"

    def test_non_square(self) -> None:
        A = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        B = torch.tensor([[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]])
        result = matrix_multiply_torch(A, B)
        expected = torch.tensor([[58.0, 64.0], [139.0, 154.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"(2x3) @ (3x2) should be [[58,64],[139,154]]; got {result}"
        )

    def test_output_shape(self) -> None:
        result = matrix_multiply_torch(torch.ones(3, 2), torch.ones(2, 4))
        assert result.shape == (3, 4), (
            f"(3,2) @ (2,4) should have shape (3,4); got {tuple(result.shape)}"
        )

    def test_order_matters(self) -> None:
        # AB != BA in general — the core lecture principle.
        A = torch.tensor([[1.0, 2.0], [0.0, 1.0]])  # shear
        B = torch.tensor([[2.0, 0.0], [0.0, 1.0]])  # stretch x
        AB = matrix_multiply_torch(A, B)
        BA = matrix_multiply_torch(B, A)
        expected_ab = torch.tensor([[2.0, 2.0], [0.0, 1.0]])
        expected_ba = torch.tensor([[2.0, 4.0], [0.0, 1.0]])
        assert torch.allclose(AB, expected_ab, atol=1e-5), f"A@B should be [[2,2],[0,1]]; got {AB}"
        assert torch.allclose(BA, expected_ba, atol=1e-5), f"B@A should be [[2,4],[0,1]]; got {BA}"


@pytest.mark.torch
class TestMatrixTransposeTorch:
    def test_two_by_three(self) -> None:
        A = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        result = matrix_transpose_torch(A)
        expected = torch.tensor([[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"Transpose of [[1,2,3],[4,5,6]] should be [[1,4],[2,5],[3,6]]; got {result}"
        )

    def test_square(self) -> None:
        A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        result = matrix_transpose_torch(A)
        expected = torch.tensor([[1.0, 3.0], [2.0, 4.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"Transpose of [[1,2],[3,4]] = [[1,3],[2,4]]; got {result}"
        )

    def test_double_transpose_is_identity(self) -> None:
        A = torch.randn(3, 5)
        result = matrix_transpose_torch(matrix_transpose_torch(A))
        assert torch.allclose(result, A, atol=1e-5), (
            "Transposing twice should give the original matrix"
        )

    def test_shape(self) -> None:
        result = matrix_transpose_torch(torch.ones(2, 4))
        assert result.shape == (4, 2), (
            f"Transposed (2,4) should have shape (4,2); got {tuple(result.shape)}"
        )

    def test_returns_tensor(self) -> None:
        result = matrix_transpose_torch(torch.eye(2))
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )


# ── Part 2b: Harder Problems ──────────────────────────────────────────────────


@pytest.mark.torch
class TestCosineSimilarity:
    def test_identical_vectors(self) -> None:
        u = torch.tensor([1.0, 2.0, 3.0])
        result = cosine_similarity(u, u)
        assert abs(result - 1.0) < 1e-5, (
            f"Cosine similarity of a vector with itself should be 1.0; got {result}"
        )

    def test_perpendicular_vectors(self) -> None:
        u = torch.tensor([1.0, 0.0])
        v = torch.tensor([0.0, 1.0])
        result = cosine_similarity(u, v)
        assert abs(result - 0.0) < 1e-5, (
            f"Perpendicular unit vectors should have cosine similarity 0; got {result}"
        )

    def test_opposite_vectors(self) -> None:
        u = torch.tensor([1.0, 2.0])
        v = torch.tensor([-1.0, -2.0])
        result = cosine_similarity(u, v)
        assert abs(result - (-1.0)) < 1e-5, (
            f"Opposite vectors should have cosine similarity -1; got {result}"
        )

    def test_known_value(self) -> None:
        # [1, 0] vs [1, 1]: angle is 45 degrees, cos(45) = sqrt(2)/2
        u = torch.tensor([1.0, 0.0])
        v = torch.tensor([1.0, 1.0])
        result = cosine_similarity(u, v)
        expected = 1.0 / (2.0**0.5)
        assert abs(result - expected) < 1e-5, (
            f"cos_sim([1,0], [1,1]) = 1/sqrt(2) = {expected:.4f}; got {result}"
        )

    def test_zero_vector_raises(self) -> None:
        with pytest.raises(ValueError):
            cosine_similarity(torch.zeros(3), torch.tensor([1.0, 2.0, 3.0]))

    def test_returns_python_float(self) -> None:
        u = torch.tensor([1.0, 0.0])
        v = torch.tensor([0.0, 1.0])
        result = cosine_similarity(u, v)
        assert isinstance(result, float), (
            f"Return type should be Python float; got {type(result).__name__}"
        )


@pytest.mark.torch
class TestRowNormalize:
    def test_rows_have_unit_norm(self) -> None:
        A = torch.tensor([[3.0, 4.0], [5.0, 12.0], [1.0, 0.0]])
        result = row_normalize(A)
        row_norms = torch.linalg.norm(result, dim=1)
        assert torch.allclose(row_norms, torch.ones(3), atol=1e-5), (
            f"Every row of the result should have norm 1; got row norms {row_norms}"
        )

    def test_basic_values(self) -> None:
        A = torch.tensor([[3.0, 4.0]])
        result = row_normalize(A)
        expected = torch.tensor([[0.6, 0.8]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"row_normalize([[3,4]]) should be [[0.6, 0.8]]; got {result}"
        )

    def test_shape_preserved(self) -> None:
        A = torch.randn(4, 5)
        result = row_normalize(A)
        assert result.shape == A.shape, (
            f"row_normalize should preserve shape; input {A.shape}, got {result.shape}"
        )

    def test_direction_preserved(self) -> None:
        A = torch.tensor([[2.0, 0.0], [0.0, 5.0]])
        result = row_normalize(A)
        expected = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"Normalizing should keep each row's direction; got {result}"
        )

    def test_zero_row_raises(self) -> None:
        A = torch.tensor([[1.0, 2.0], [0.0, 0.0]])
        with pytest.raises(ValueError):
            row_normalize(A)

    def test_returns_tensor(self) -> None:
        result = row_normalize(torch.tensor([[1.0, 0.0]]))
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )


@pytest.mark.torch
class TestPairwiseDistances:
    def test_known_values(self) -> None:
        A = torch.tensor([[0.0, 0.0], [3.0, 4.0]])
        result = pairwise_distances(A)
        expected = torch.tensor([[0.0, 5.0], [5.0, 0.0]])
        assert torch.allclose(result, expected, atol=1e-5), (
            f"pairwise_distances([[0,0],[3,4]]) should be [[0,5],[5,0]]; got {result}"
        )

    def test_three_points(self) -> None:
        A = torch.tensor([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
        result = pairwise_distances(A)
        expected = torch.tensor(
            [
                [0.0, 1.0, 1.0],
                [1.0, 0.0, 2.0**0.5],
                [1.0, 2.0**0.5, 0.0],
            ]
        )
        assert torch.allclose(result, expected, atol=1e-5), (
            f"Distances between unit-square corners are wrong; got {result}"
        )

    def test_diagonal_is_zero(self) -> None:
        A = torch.randn(4, 3)
        result = pairwise_distances(A)
        assert torch.allclose(result.diagonal(), torch.zeros(4), atol=1e-5), (
            f"Diagonal of pairwise_distances should be all zeros; got {result.diagonal()}"
        )

    def test_symmetry(self) -> None:
        A = torch.randn(5, 3)
        result = pairwise_distances(A)
        assert torch.allclose(result, result.mT, atol=1e-5), (
            "pairwise_distances must be symmetric: dist(i,j) == dist(j,i)"
        )

    def test_output_shape(self) -> None:
        A = torch.ones(6, 4)
        result = pairwise_distances(A)
        assert result.shape == (6, 6), (
            f"pairwise_distances of (6,4) tensor should have shape (6,6); got {result.shape}"
        )

    def test_returns_tensor(self) -> None:
        result = pairwise_distances(torch.eye(3))
        assert isinstance(result, torch.Tensor), (
            f"Return type should be torch.Tensor, not {type(result).__name__}"
        )
