"""HW01 — Linear Algebra

Part 1: Pure-Python implementations (no torch, no numpy).
  Vectors are list[float]; matrices are list[list[float]] (row-major order).

Part 2: The same operations again, this time as PyTorch one-liners — no manual
  loops. The point is to see that PyTorch does exactly the math you wrote by
  hand in Part 1, just faster.

Run tests:   uv run pytest
Check score: uv run python score.py
"""

from __future__ import annotations

import math

import torch

# ── Part 1: From Scratch ──────────────────────────────────────────────────────


def vector_add(u: list[float], v: list[float]) -> list[float]:
    """Return the element-wise sum of two vectors.

    Both vectors must have the same length.

    Args:
        u: First vector.
        v: Second vector, same length as u.

    Returns:
        A new vector w where w[i] = u[i] + v[i].

    Example:
        >>> vector_add([1.0, 2.0], [3.0, 4.0])
        [4.0, 6.0]

    Hint:
        Think about how to iterate over two lists simultaneously, pairing their
        elements at each position.
    """
    raise NotImplementedError("Implement vector_add()")


def scalar_multiply(c: float, v: list[float]) -> list[float]:
    """Scale every element of a vector by a scalar.

    Args:
        c: The scalar multiplier.
        v: The vector to scale.

    Returns:
        A new vector w where w[i] = c * v[i].

    Example:
        >>> scalar_multiply(3.0, [1.0, 2.0, 3.0])
        [3.0, 6.0, 9.0]

    Hint:
        You know how to visit every element in a list. What would you do
        to each one?
    """
    raise NotImplementedError("Implement scalar_multiply()")


def dot_product(u: list[float], v: list[float]) -> float:
    """Compute the dot product (inner product) of two vectors.

    The dot product is the sum of element-wise products:
        dot(u, v) = u[0]*v[0] + u[1]*v[1] + ... + u[n-1]*v[n-1]

    Args:
        u: First vector.
        v: Second vector, same length as u.

    Returns:
        A single float — the dot product of u and v.

    Example:
        >>> dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
        32.0

    Hint:
        You already know how to pair elements from two lists. The dot product
        needs one more step: combine those products into a single number.
    """
    raise NotImplementedError("Implement dot_product()")


def vector_magnitude(v: list[float]) -> float:
    """Compute the Euclidean (L2) magnitude (length) of a vector.

    magnitude(v) = sqrt(v[0]^2 + v[1]^2 + ... + v[n-1]^2)

    Args:
        v: The input vector.

    Returns:
        A non-negative float — the magnitude of v.

    Example:
        >>> vector_magnitude([3.0, 4.0])
        5.0

    Hint:
        Look at the formula in the docstring — it expresses magnitude in terms
        of an operation you've already implemented.
    """
    raise NotImplementedError("Implement vector_magnitude()")


def normalize_vector(v: list[float]) -> list[float]:
    """Return the unit vector in the same direction as v.

    A unit vector has magnitude 1. To normalize, divide each element by the
    magnitude of v.

    Args:
        v: The vector to normalize.

    Returns:
        A new vector with magnitude 1, pointing in the same direction as v.

    Raises:
        ValueError: If v is the zero vector (magnitude == 0).

    Example:
        >>> normalize_vector([3.0, 4.0])
        [0.6, 0.8]

    Hint:
        You have all the pieces from earlier in Part 1. Think about what needs
        to be true about the magnitude before dividing, and what should happen
        if that condition fails.
    """
    raise NotImplementedError("Implement normalize_vector()")


def matrix_add(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Return the element-wise sum of two matrices.

    Both matrices must have identical dimensions (same number of rows and
    the same number of columns in each row).

    Args:
        A: First matrix (list of rows).
        B: Second matrix, same shape as A.

    Returns:
        A new matrix C where C[i][j] = A[i][j] + B[i][j].

    Example:
        >>> matrix_add([[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]])
        [[6.0, 8.0], [10.0, 12.0]]

    Hint:
        You have a function that adds two vectors. How could you apply it to
        each pair of corresponding rows?
    """
    raise NotImplementedError("Implement matrix_add()")


def matrix_vector_multiply(A: list[list[float]], v: list[float]) -> list[float]:
    """Multiply a matrix A by a column vector v.

    The i-th element of the output is the dot product of the i-th row of A
    with v:
        result[i] = dot(A[i], v)

    Args:
        A: A matrix with shape (m, n) — m rows, n columns.
        v: A vector of length n.

    Returns:
        A vector of length m.

    Example:
        >>> matrix_vector_multiply([[1.0, 2.0], [3.0, 4.0]], [1.0, 1.0])
        [3.0, 7.0]

    Hint:
        The docstring gives you the mathematical rule. You have a function that
        computes exactly what each output element requires — apply it across the
        rows.
    """
    raise NotImplementedError("Implement matrix_vector_multiply()")


def matrix_multiply(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Multiply two matrices A and B.

    If A has shape (m, k) and B has shape (k, n), the result has shape (m, n).
    The (i, j) entry of the result is:
        C[i][j] = dot product of row i of A with column j of B

    Args:
        A: Matrix with shape (m, k).
        B: Matrix with shape (k, n).

    Returns:
        Matrix C with shape (m, n).

    Example:
        >>> matrix_multiply([[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]])
        [[19.0, 22.0], [43.0, 50.0]]

    Hint:
        The hard part is accessing B's columns. Think about what operation
        could turn columns into something easier to work with. You may implement
        the next helper first.
    """
    raise NotImplementedError("Implement matrix_multiply()")


def matrix_transpose(A: list[list[float]]) -> list[list[float]]:
    """Return the transpose of matrix A.

    The transpose swaps rows and columns: T[i][j] = A[j][i].

    Args:
        A: A matrix with shape (m, n).

    Returns:
        The transposed matrix with shape (n, m).

    Example:
        >>> matrix_transpose([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]

    Hint:
        Column j of A is the j-th element of every row. A nested loop over the
        output's indices does this directly. For a shorter route: the same
        builtin you used to walk two lists in lockstep accepts more than two
        sequences — the obstacle is that you have one list of rows rather than
        separate arguments. Either way, check the type of what you build
        against this function's return annotation before you trust it.
    """
    raise NotImplementedError("Implement matrix_transpose()")


# ── Part 2: PyTorch Mirrors ───────────────────────────────────────────────────
#
# Each function below repeats one Part 1 operation, but on torch.Tensor inputs.
# Every implementation is 1-3 lines using PyTorch operations from the lecture
# cheat sheet — no loops, no list comprehensions.


def dot_product_torch(u: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    """Same operation as dot_product (Part 1), now using PyTorch.

    Args:
        u: 1-D tensor.
        v: 1-D tensor, same length as u.

    Returns:
        A 0-dimensional tensor holding the dot product of u and v.

    Example:
        >>> dot_product_torch(torch.tensor([1.0, 2.0, 3.0]), torch.tensor([4.0, 5.0, 6.0]))
        tensor(32.)

    Hint:
        In Part 1 this took you a comprehension and a sum. PyTorch has a single
        function for it — check the lecture cheat sheet.
    """
    raise NotImplementedError("Implement dot_product_torch()")


def vector_magnitude_torch(v: torch.Tensor) -> torch.Tensor:
    """Same operation as vector_magnitude (Part 1), now using PyTorch.

    Args:
        v: 1-D tensor.

    Returns:
        A 0-dimensional tensor holding the Euclidean (L2) magnitude of v.

    Example:
        >>> vector_magnitude_torch(torch.tensor([3.0, 4.0]))
        tensor(5.)

    Hint:
        The norm of a vector is such a common operation that torch.linalg
        provides it directly.
    """
    raise NotImplementedError("Implement vector_magnitude_torch()")


def normalize_vector_torch(v: torch.Tensor) -> torch.Tensor:
    """Same operation as normalize_vector (Part 1), now using PyTorch.

    Args:
        v: 1-D tensor.

    Returns:
        A new 1-D tensor with magnitude 1, pointing in the same direction as v.

    Raises:
        ValueError: If v is the zero vector (magnitude == 0).

    Example:
        >>> normalize_vector_torch(torch.tensor([3.0, 4.0]))
        tensor([0.6000, 0.8000])

    Hint:
        Dividing a tensor by a scalar divides every element — no loop needed.
        Remember to check for the zero vector first, just like in Part 1.
    """
    raise NotImplementedError("Implement normalize_vector_torch()")


def matrix_vector_multiply_torch(A: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    """Same operation as matrix_vector_multiply (Part 1), now using PyTorch.

    Args:
        A: 2-D tensor of shape (m, n).
        v: 1-D tensor of length n.

    Returns:
        1-D tensor of length m, where element i is the dot product of
        row i of A with v.

    Example:
        >>> A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        >>> matrix_vector_multiply_torch(A, torch.tensor([1.0, 1.0]))
        tensor([3., 7.])

    Hint:
        The @ operator from lecture handles matrix-vector products too.
    """
    raise NotImplementedError("Implement matrix_vector_multiply_torch()")


def matrix_multiply_torch(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    """Same operation as matrix_multiply (Part 1), now using PyTorch.

    In Part 1 this took you a transpose plus a double comprehension of dot
    products. PyTorch does all of that in one operator.

    Args:
        A: 2-D tensor of shape (m, k).
        B: 2-D tensor of shape (k, n).

    Returns:
        2-D tensor of shape (m, n) — the matrix product AB.

    Example:
        >>> A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        >>> B = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
        >>> matrix_multiply_torch(A, B)
        tensor([[19., 22.],
                [43., 50.]])
    """
    raise NotImplementedError("Implement matrix_multiply_torch()")


def matrix_transpose_torch(A: torch.Tensor) -> torch.Tensor:
    """Same operation as matrix_transpose (Part 1), now using PyTorch.

    Args:
        A: 2-D tensor of shape (m, n).

    Returns:
        2-D tensor of shape (n, m) — the transpose of A.

    Example:
        >>> matrix_transpose_torch(torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
        tensor([[1., 4.],
                [2., 5.],
                [3., 6.]])

    Hint:
        In Part 1 this took you a whole comprehension. In PyTorch the transpose
        is a single attribute access — see the lecture cheat sheet.
    """
    raise NotImplementedError("Implement matrix_transpose_torch()")


# ── Part 2b: Harder Problems ──────────────────────────────────────────────────
#
# These three functions go beyond mirroring Part 1: compare two vectors, normalize
# a matrix row by row, and compute distances between all pairs of rows. A loop-based solution
# earns full credit; a vectorized (loop-free) solution is shorter, faster, and
# worth attempting once the loop version works.


def cosine_similarity(u: torch.Tensor, v: torch.Tensor) -> float:
    """Compute the cosine similarity between two 1-D tensors.

    Cosine similarity measures the angle between two vectors:

        cos_sim(u, v) = (u . v) / (||u|| * ||v||)

    It ranges from -1 (opposite directions) to 1 (same direction).
    A value of 0 means the vectors are perpendicular. This is the standard
    way to compare embeddings, and it returns in Module 6.

    Args:
        u: 1-D tensor.
        v: 1-D tensor, same length as u.

    Returns:
        A Python float in [-1, 1].

    Raises:
        ValueError: If either u or v is the zero vector.

    Example:
        >>> cosine_similarity(torch.tensor([1.0, 0.0]), torch.tensor([1.0, 0.0]))
        1.0
        >>> cosine_similarity(torch.tensor([1.0, 0.0]), torch.tensor([0.0, 1.0]))
        0.0

    Hint:
        Each term in the formula maps to one operation you already wrote in
        Part 2. Handle the zero-vector case before dividing. Do not use
        torch.nn.functional.cosine_similarity.
    """
    raise NotImplementedError("Implement cosine_similarity()")


def row_normalize(A: torch.Tensor) -> torch.Tensor:
    """Normalize each row of a matrix to unit length.

    For a matrix with m rows, returns a new matrix where every row
    has Euclidean norm equal to 1. Think of each row as one data point:
    this rescales every point onto the unit sphere, so that comparisons
    between rows depend only on direction, not magnitude.

    Args:
        A: 2-D tensor of shape (m, n).

    Returns:
        2-D tensor of shape (m, n) where each row has norm 1.

    Raises:
        ValueError: If any row of A is the zero vector.

    Example:
        >>> A = torch.tensor([[3.0, 4.0], [0.0, 2.0]])
        >>> row_normalize(A)
        tensor([[0.6000, 0.8000],
                [0.0000, 1.0000]])

    Hint:
        Each row needs its own norm — torch.linalg.norm can reduce along a
        chosen axis rather than over the whole tensor. Once you have those m
        norms, scaling each row by its own norm is a broadcasting question:
        what shape must the norms have to line up with the rows of A, and what
        shape does norm() hand you by default? Also: a zero row has norm 0, so
        check all m norms at once before dividing (a comparison on a tensor
        gives you a tensor of booleans) and raise ValueError.
        Do not use torch.nn.functional.normalize.
    """
    raise NotImplementedError("Implement row_normalize()")


def pairwise_distances(A: torch.Tensor) -> torch.Tensor:
    """Compute the pairwise Euclidean distance between every row of A.

    For a matrix with m rows, returns an (m, m) matrix where entry (i, j)
    is the Euclidean distance between row i and row j of A. The diagonal
    is all zeros (distance from a row to itself) and the matrix is
    symmetric. "How far apart is every pair of data points?" is a question
    you will ask constantly in this course.

    Args:
        A: 2-D tensor of shape (m, n).

    Returns:
        2-D tensor of shape (m, m).

    Example:
        >>> A = torch.tensor([[0.0, 0.0], [3.0, 4.0]])
        >>> pairwise_distances(A)
        tensor([[0., 5.],
                [5., 0.]])

    Hint:
        A double loop over the rows works. For the vectorized version, think
        about how to set up one subtraction that computes all pairs at once:
        subtraction of differently-shaped tensors can broadcast — what shapes
        would make row i of one copy and row j of the other copy line up for
        all i and j simultaneously? torch.unsqueeze (which inserts a length-1
        axis you can broadcast along) is the tool for making those two copies;
        you still have to decide which axis each copy gets and how to collapse
        the result into distances. Do not use torch.cdist.
    """
    raise NotImplementedError("Implement pairwise_distances()")
