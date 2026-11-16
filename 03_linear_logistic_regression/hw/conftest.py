"""Pytest configuration for HW03.

Sets deterministic seeds for reproducibility, blocks the sklearn linear-model
shortcut, and enforces that regression.py does not use torch.autograd
(students must compute gradients manually using the formulas from lecture).
"""

from __future__ import annotations

import ast
import random
from pathlib import Path

import pytest
import torch

# ── Deterministic seeds ────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def set_seed() -> None:
    """Set deterministic seeds before every test."""
    random.seed(42)
    torch.manual_seed(42)
    torch.backends.cudnn.deterministic = True


# ── Source loading ─────────────────────────────────────────────────────────────


_REGRESSION_SOURCE = (Path(__file__).parent / "regression.py").read_text()


def _uses_forbidden_import(source: str, forbidden: str) -> bool:
    """Return True if `source` imports `forbidden` (as module or submodule)."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == forbidden or alias.name.startswith(forbidden + "."):
                    return True
        elif isinstance(node, ast.ImportFrom):
            if node.module and (
                node.module == forbidden or node.module.startswith(forbidden + ".")
            ):
                return True
    return False


# ── Block sklearn.linear_model ─────────────────────────────────────────────────
# Using sklearn.linear_model.LinearRegression / LogisticRegression bypasses the
# point of the assignment (implementing the model from scratch).


@pytest.fixture(autouse=True)
def block_sklearn_linear_model() -> None:
    """Fail if regression.py imports from sklearn.linear_model."""
    if _uses_forbidden_import(_REGRESSION_SOURCE, "sklearn.linear_model"):
        pytest.fail(
            "regression.py must NOT import from sklearn.linear_model. "
            "Implement LinearRegression and LogisticRegression from scratch."
        )


# ── Block torch.autograd in actual code (not docstrings/comments) ──────────────
# Students must compute every gradient by hand using the formulas in spec.pdf.
# AST walk so we skip docstrings and comments.


def _autograd_violation(source: str) -> str | None:
    """Return a description of the first autograd usage found, or None."""
    # Imports like `from torch.autograd import grad` or `import torch.autograd as ag`.
    if _uses_forbidden_import(source, "torch.autograd"):
        return "torch.autograd (import)"
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        # Calls like x.backward()
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "backward":
                return ".backward()"
        # Keyword arguments like requires_grad=True
        if isinstance(node, ast.keyword) and node.arg == "requires_grad":
            return "requires_grad="
        # Attribute access like .requires_grad or torch.autograd.X
        if isinstance(node, ast.Attribute):
            if node.attr == "requires_grad":
                return ".requires_grad"
            if node.attr == "autograd":
                return "torch.autograd"
        # Method calls like .requires_grad_(True)
        if isinstance(node, ast.Attribute) and node.attr == "requires_grad_":
            return ".requires_grad_()"
    return None


@pytest.fixture(autouse=True)
def block_autograd_in_regression_module() -> None:
    """Fail if regression.py uses torch.autograd anywhere in actual code."""
    violation = _autograd_violation(_REGRESSION_SOURCE)
    if violation is not None:
        pytest.fail(
            f"regression.py must NOT use {violation}. "
            "Compute every gradient manually using the formulas in spec.pdf / "
            "the Lesson 3 derivation. The whole point of HW03 is that you "
            "are the autograd engine."
        )


# ── Block built-in sigmoid shortcuts ───────────────────────────────────────────
# `def sigmoid(z): return torch.sigmoid(z)` would pass the sigmoid tests but
# bypasses the §2 learning goal of implementing the formula yourself. The same
# goes for torch.nn.functional.sigmoid (often aliased as F.sigmoid) and
# torch.special.expit.

_SIGMOID_SHORTCUTS: set[str] = {
    "torch.sigmoid",
    "torch.nn.functional.sigmoid",
    "torch.special.expit",
}


def _dotted_name(node: ast.expr) -> str | None:
    """Reconstruct a dotted name like 'torch.nn.functional.sigmoid', if possible."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def _sigmoid_shortcut(source: str) -> str | None:
    """Return the forbidden built-in sigmoid used in `source`, or None."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    # Map import aliases to full module paths (e.g. F -> torch.nn.functional).
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    aliases[alias.asname] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                # e.g. `from torch.nn.functional import sigmoid`
                if f"{node.module}.{alias.name}" in _SIGMOID_SHORTCUTS:
                    return f"{node.module}.{alias.name}"
    # Attribute chains like torch.sigmoid(...) or F.sigmoid(...).
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            dotted = _dotted_name(node)
            if dotted is None:
                continue
            root, _, rest = dotted.partition(".")
            expanded = aliases.get(root, root) + (("." + rest) if rest else "")
            if expanded in _SIGMOID_SHORTCUTS:
                return expanded

    # Tensor-method form: z.sigmoid(), z.sigmoid_(), z.expit(),
    # torch.Tensor.sigmoid(z). `_dotted_name` above only reconstructs chains
    # rooted at a Name, so a method call on an expression slips through - and
    # `z.sigmoid()` is numerically identical to the required formula, so it
    # passes every TestSigmoid case while bypassing the section 2 learning
    # goal entirely. Exempt `self.<attr>` so a student's own helper method is
    # not falsely flagged.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        if func.attr not in {"sigmoid", "sigmoid_", "expit"}:
            continue
        if isinstance(func.value, ast.Name) and func.value.id == "self":
            continue
        return f".{func.attr}() (tensor method)"
    return None


@pytest.fixture(autouse=True)
def block_torch_sigmoid_shortcut() -> None:
    """Fail if regression.py uses a built-in sigmoid (defeats §2 learning goal)."""
    shortcut = _sigmoid_shortcut(_REGRESSION_SOURCE)
    if shortcut is not None:
        pytest.fail(
            f"regression.py must NOT use {shortcut}. "
            "Implement sigmoid from the formula in spec.pdf §2."
        )
