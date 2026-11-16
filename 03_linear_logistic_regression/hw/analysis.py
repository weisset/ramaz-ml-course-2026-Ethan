"""HW03 — Analysis: Regression on real datasets.

Implement the five helper functions below, then run this script to generate
the results you reference in writeup.md:

    uv run python analysis.py

The script trains both models and saves two plots to the hw/ directory:
    loss_curve.png         — training loss vs. epoch for linear regression
    decision_boundary.png  — logistic regression decision boundary on Iris

Prerequisites: complete regression.py first.
"""

from __future__ import annotations

import torch
from sklearn.datasets import fetch_california_housing, load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from regression import LinearRegression, LogisticRegression

# ── Part 3a: Regression data + training ────────────────────────────────────────


def load_regression_data() -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """See spec.pdf."""
    raise NotImplementedError("Implement load_regression_data()")


def train_linear_model(
    X_train: torch.Tensor,
    y_train: torch.Tensor,
    lr: float = 0.01,
    epochs: int = 200,
) -> tuple[LinearRegression, list[float]]:
    """See spec.pdf."""
    raise NotImplementedError("Implement train_linear_model()")


# ── Part 3b: Classification data + training ────────────────────────────────────


def load_classification_data() -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """See spec.pdf."""
    raise NotImplementedError("Implement load_classification_data()")


def majority_class_baseline(y: torch.Tensor) -> float:
    """See spec.pdf section 6.4 (majority_class_baseline)."""
    raise NotImplementedError("Implement majority_class_baseline()")


def train_logistic_model(
    X_train: torch.Tensor,
    y_train: torch.Tensor,
    lr: float = 0.5,
    epochs: int = 300,
) -> tuple[LogisticRegression, list[float]]:
    """See spec.pdf."""
    raise NotImplementedError("Implement train_logistic_model()")


# ── Main: run experiments and produce plots ────────────────────────────────────

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    print("=" * 60)
    print("Part 3a: Linear Regression on California Housing")
    print("=" * 60)

    X_train, X_test, y_train, y_test = load_regression_data()
    print(f"Training set: {X_train.shape[0]} examples, {X_train.shape[1]} features")
    print(f"Test set:     {X_test.shape[0]} examples")

    fig, ax = plt.subplots(figsize=(8, 5))
    for lr in (2e-5, 0.02, 1.0):
        model, history = train_linear_model(X_train, y_train, lr=lr, epochs=200)
        ax.plot(range(1, len(history) + 1), history, label=f"lr={lr:g}")
        print(
            f"  lr={lr:g}: first={history[0]:.3g}, min={min(history):.3g}, last={history[-1]:.3g}"
        )
        if lr == 0.02:
            test_loss = model.loss(model.predict(X_test), y_test)
            print(f"    Test loss after training: {test_loss.item():.4f}")

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Half mean squared error (log scale)")
    ax.set_yscale("log")
    ax.set_title("Linear Regression: Training Loss vs. Epoch")
    ax.legend()
    fig.tight_layout()
    fig.savefig("loss_curve.png", dpi=150)
    print("\nSaved: loss_curve.png")

    print()
    print("=" * 60)
    print("Part 3b: Logistic Regression on Iris (setosa vs. versicolor)")
    print("=" * 60)

    X_cls_train, X_cls_test, y_cls_train, y_cls_test = load_classification_data()
    print(f"Training set: {X_cls_train.shape[0]} examples, {X_cls_train.shape[1]} features")

    baseline_train = majority_class_baseline(y_cls_train)
    majority_label = torch.bincount(y_cls_train.long()).argmax().item()
    baseline_test = (y_cls_test == majority_label).float().mean().item()
    print(f"Majority class in training data: {majority_label} ({baseline_train:.1%} of labels)")
    print(f"Training-majority baseline on test set: {baseline_test:.1%}")

    log_model, log_history = train_logistic_model(X_cls_train, y_cls_train, lr=0.5, epochs=300)
    print(f"First loss: {log_history[0]:.4f}, Last loss: {log_history[-1]:.4f}")

    correct = log_model.predict(X_cls_test) == y_cls_test
    accuracy = correct.float().mean().item()
    errors = (~correct).sum().item()
    print(f"Test accuracy: {accuracy:.1%} ({errors} errors in {y_cls_test.numel()} examples)")

    # Decision boundary in (x_1, x_2): w_1·x_1 + w_2·x_2 + b = 0
    w1, w2, bias = log_model.w[0].item(), log_model.w[1].item(), log_model.b.item()
    print(f"\nLearned weights: w = [{w1:.4f}, {w2:.4f}]")
    print(f"Learned bias:    b = {bias:.4f}")
    print("\n--- Decision boundary ---")
    print(f"  {w1:.4f}·x1 + {w2:.4f}·x2 + {bias:.4f} = 0")

    # Plot decision boundary
    fig2, ax2 = plt.subplots(figsize=(7, 6))
    x1 = X_cls_test[:, 0]
    x2 = X_cls_test[:, 1]
    xx1, xx2 = torch.meshgrid(
        torch.linspace(x1.min().item() - 0.5, x1.max().item() + 0.5, 200),
        torch.linspace(x2.min().item() - 0.5, x2.max().item() + 0.5, 200),
        indexing="ij",
    )
    grid = torch.stack((xx1.flatten(), xx2.flatten()), dim=1)
    probabilities = log_model.predict_proba(grid).reshape(xx1.shape)
    x_grid, y_grid, p_grid = xx1.tolist(), xx2.tolist(), probabilities.tolist()
    ax2.contourf(
        x_grid, y_grid, p_grid, levels=[0, 0.5, 1], alpha=0.2, colors=["lightblue", "lightsalmon"]
    )
    ax2.contour(x_grid, y_grid, p_grid, levels=[0.5], colors=["navy"])

    for label, name, color, marker in (
        (0, "Setosa", "steelblue", "o"),
        (1, "Versicolor", "salmon", "s"),
    ):
        mask = y_cls_test == label
        ax2.scatter(
            x1[mask].tolist(),
            x2[mask].tolist(),
            c=color,
            marker=marker,
            label=name,
            edgecolors="black",
            linewidths=0.5,
        )
    ax2.set_xlabel("Sepal length (standardized)")
    ax2.set_ylabel("Sepal width (standardized)")
    ax2.set_title("Logistic Regression Decision Boundary on the Iris Test Set")
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig("decision_boundary.png", dpi=150)
    print("\nSaved: decision_boundary.png")
    print("\nAll done. Use these results to answer the questions in writeup.md.")
