"""HW03 - Linear and Logistic Regression.

Implement the spec in spec.pdf. The public API of this file is:

    sigmoid(z)
    LinearModel       (shared base class)
    LinearRegression  (subclass of LinearModel)
    LogisticRegression(subclass of LinearModel)

Restrictions: no torch.autograd, no .backward(), no sklearn.linear_model.

Run tests:   uv run pytest
Check score: uv run python score.py
"""

from __future__ import annotations

import torch


def sigmoid(z: torch.Tensor) -> torch.Tensor:
    """See spec.pdf section 2 (standalone sigmoid)."""
    raise NotImplementedError("Implement sigmoid()")


class LinearModel:
    """See spec.pdf section 3 (shared LinearModel base class)."""


class LinearRegression(LinearModel):
    """See spec.pdf section 4 (LinearRegression: forward + MSE loss)."""


class LogisticRegression(LinearModel):
    """See spec.pdf section 5 (LogisticRegression: forward, BCE, predict)."""
