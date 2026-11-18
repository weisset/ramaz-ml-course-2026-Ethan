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
import torch # pyright: ignore[reportMissingImports]


def sigmoid(z: torch.Tensor) -> torch.Tensor:
    """See spec.pdf section 2 (standalone sigmoid)."""
    return 1 / (1 + torch.exp(-z))


class LinearModel:
    """See spec.pdf section 3 (shared LinearModel base class)."""
    
    def __init__(self, n_features: int, lr: float = 0.1) -> None:
        
        self.w = torch.tensor([0] * n_features, dtype = torch.float32)
        self.b = torch.tensor(0.0, dtype = torch.float32)
        self.lr = lr

    def gradient(self, X: torch.Tensor, y_true: torch.Tensor, y_pred: torch.Tensor) \
        -> tuple[torch.Tensor, torch.Tensor]:
        
        return (
            torch.tensor((X.T @ (y_pred - y_true)) / y_pred.numel()),
            torch.tensor((torch.ones((y_pred.numel())).T @ (y_pred - y_true)) / y_pred.numel())
        )

    def fit(self, X: torch.Tensor, y: torch.Tensor, epochs: int = 200) -> list[float]:

        loss_history = []

        for i in range(epochs):
            y_pred = self.predict(X)
            loss = self.loss(y_pred, y) # pyright: ignore[reportAttributeAccessIssue]
            loss_history.append(loss.item())
            grads = self.gradient(X, y, y_pred)

            self.w -= self.lr * grads[0]
            self.b -= self.lr * grads[1]

        return loss_history

    def predict(self, X: torch.Tensor) -> torch.Tensor:

        return self.forward(X) # pyright: ignore[reportAttributeAccessIssue]


class LinearRegression(LinearModel):
    """See spec.pdf section 4 (LinearRegression: forward + MSE loss)."""

    def forward(self, X: torch.Tensor) -> torch.Tensor:

        return X @ self.w + self.b

    def loss(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:

        return torch.linalg.vector_norm(y_pred - y_true) ** 2 / (2 * torch.numel(y_pred))

class LogisticRegression(LinearModel):
    """See spec.pdf section 5 (LogisticRegression: forward, BCE, predict)."""

    def forward(self, X: torch.Tensor) -> torch.Tensor:

        return sigmoid(X @ self.w + self.b)

    def loss(self, y_pred: torch.Tensor, y_true: torch.Tensor) -> torch.Tensor:

        epsilon = 10**(-7)

        y_pred.clamp_(min = epsilon, max = 1 - epsilon)

        return -torch.sum(
            y_true * torch.log(y_pred)
            +
            (1 - y_true) * torch.log(1 - y_pred)
        ) / torch.numel(y_pred)

    def predict_proba(self, X: torch.Tensor) -> torch.Tensor:

        return self.forward(X)

    def predict(self, X: torch.Tensor) -> torch.Tensor:

        return torch.round(self.predict_proba(X))