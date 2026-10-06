"""HW01 — Part 3: Matrices as Transformations

Implement the four helper functions below. Each one builds (or applies) a 2x2
transformation matrix from the lecture's "Geometric View" section.

Then run this script to generate the figure for your writeup:

    uv run python analysis.py

It saves transforms.png and prints a few values. Use both to answer the
questions in writeup.md. The plotting code at the bottom is provided for you —
do not modify it.
"""

from __future__ import annotations

import math

import torch


def rotation_matrix(degrees: float) -> torch.Tensor:
    """Build the 2x2 matrix that rotates a 2D vector counterclockwise.

    From lecture, rotation by angle theta is:

        R(theta) = [[cos(theta), -sin(theta)],
                    [sin(theta),  cos(theta)]]

    Args:
        degrees: Rotation angle in degrees (counterclockwise).

    Returns:
        2-D tensor of shape (2, 2), with dtype torch.float32 to match
        the provided plotting data.

    Example:
        >>> rotation_matrix(90.0)
        tensor([[ 0., -1.],
                [ 1.,  0.]])
        # (up to tiny floating-point error, e.g. -8.7e-09 instead of 0)

    Hint:
        The lecture's R(theta) is in radians, but this function takes degrees —
        the `math` module has a converter. Then assemble those four entries
        into a 2x2 tensor.
    """
    raise NotImplementedError("Implement rotation_matrix()")


def scaling_matrix(sx: float, sy: float) -> torch.Tensor:
    """Build the 2x2 matrix that scales x by sx and y by sy.

    From lecture, this is the diagonal matrix:

        S = [[sx, 0],
             [0, sy]]

    Args:
        sx: Scale factor for the x-coordinate.
        sy: Scale factor for the y-coordinate.

    Returns:
        2-D tensor of shape (2, 2), with dtype torch.float32 to match
        the provided plotting data.

    Example:
        >>> scaling_matrix(2.0, 0.5)
        tensor([[2.0000, 0.0000],
                [0.0000, 0.5000]])
    """
    raise NotImplementedError("Implement scaling_matrix()")


def shear_matrix(k: float) -> torch.Tensor:
    """Build the 2x2 horizontal shear matrix with shear factor k.

    A horizontal shear slides each point sideways by an amount proportional
    to its height: (x, y) becomes (x + k*y, y). As a matrix:

        H = [[1, k],
             [0, 1]]

    Args:
        k: The shear factor.

    Returns:
        2-D tensor of shape (2, 2), with dtype torch.float32 to match
        the provided plotting data.

    Example:
        >>> shear_matrix(0.8)
        tensor([[1.0000, 0.8000],
                [0.0000, 1.0000]])
    """
    raise NotImplementedError("Implement shear_matrix()")


def apply_transform(points: torch.Tensor, matrix: torch.Tensor) -> torch.Tensor:
    """Apply a 2x2 transformation matrix to every point in a set of 2D points.

    Each row of `points` is one point p, and its transformed position is the
    matrix-vector product M p. The result has the same shape as the input:
    row i of the output is M applied to row i of the input.

    Args:
        points: 2-D tensor of shape (N, 2) — one point per row.
        matrix: 2-D tensor of shape (2, 2).

    Returns:
        2-D tensor of shape (N, 2) — the transformed points, one per row.

    Example:
        >>> pts = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
        >>> apply_transform(pts, rotation_matrix(90.0))
        tensor([[ 0.,  1.],
                [-1.,  0.]])
        # (1,0) rotates to (0,1); (0,1) rotates to (-1,0)
        # (up to tiny floating-point error)

    Hint:
        The lecture writes this as M p, with the point p as a column vector.
        But `points` stores one point per ROW. Write out what a single row of
        `points @ matrix` actually computes and compare it to M p — are they
        the same? If not, what would you have to change to make each output
        row equal M applied to the corresponding input point? Your return
        value must be (N, 2), one point per row.
    """
    raise NotImplementedError("Implement apply_transform()")


# ── Teacher-provided plotting code — do not modify anything below ─────────────

if __name__ == "__main__":
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # An asymmetric arrow so flips/rotations are easy to see.
    shape = torch.tensor(
        [
            [0.0, 0.0],
            [2.0, 0.0],
            [2.0, -0.5],
            [3.0, 0.5],
            [2.0, 1.5],
            [2.0, 1.0],
            [0.0, 0.7],
        ]
    )

    R = rotation_matrix(60.0)
    S = scaling_matrix(2.0, 0.5)
    H = shear_matrix(0.8)
    RS = R @ S  # scale first, then rotate
    SR = S @ R  # rotate first, then scale

    panels = [
        ("Original", shape),
        ("Rotation 60 deg", apply_transform(shape, R)),
        ("Scaling (2, 0.5)", apply_transform(shape, S)),
        ("Shear k=0.8", apply_transform(shape, H)),
        ("R @ S (scale, then rotate)", apply_transform(shape, RS)),
        ("S @ R (rotate, then scale)", apply_transform(shape, SR)),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for ax, (title, pts) in zip(axes.flat, panels):
        closed_orig = torch.cat([shape, shape[:1]])
        closed = torch.cat([pts, pts[:1]])
        ax.plot(closed_orig[:, 0], closed_orig[:, 1], color="0.8", linewidth=1.5)
        ax.fill(closed[:, 0], closed[:, 1], color="tab:blue", alpha=0.35)
        ax.plot(closed[:, 0], closed[:, 1], color="tab:blue", linewidth=2)
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.set_xlim(-4, 6.5)
        ax.set_ylim(-3, 6)
        ax.axhline(0, color="0.6", linewidth=0.8)
        ax.axvline(0, color="0.6", linewidth=0.8)
        ax.grid(True, alpha=0.3)
    fig.suptitle("HW01 Part 3: one shape, five transformations (gray = original)")
    fig.tight_layout()
    fig.savefig("transforms.png", dpi=150)
    print("Saved transforms.png")

    torch.set_printoptions(precision=3, sci_mode=False)
    print("\nR @ S (scale, then rotate) =")
    print(RS)
    print("\nS @ R (rotate, then scale) =")
    print(SR)
    tip = shape[3]
    print(f"\nArrow tip {tip.tolist()} lands at:")
    print(f"  under R @ S: {(RS @ tip).tolist()}")
    print(f"  under S @ R: {(SR @ tip).tolist()}")
