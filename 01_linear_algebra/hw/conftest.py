from __future__ import annotations

import ast
import inspect
import random
from types import ModuleType

import pytest
import torch

# Part 1 function names that must not use PyTorch.
_PART1_FN_NAMES: list[str] = [
    "vector_add",
    "scalar_multiply",
    "dot_product",
    "vector_magnitude",
    "normalize_vector",
    "matrix_add",
    "matrix_vector_multiply",
    "matrix_multiply",
    "matrix_transpose",
]


def _torch_bound_names(tree: ast.AST) -> set[str]:
    """Collect every name bound to torch anywhere in the module.

    Covers `import torch`, `import torch as t`, `import torch.nn`,
    and `from torch import dot` / `from torch import dot as d`.
    """
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "torch" or alias.name.startswith("torch."):
                    names.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "torch" or module.startswith("torch."):
                for alias in node.names:
                    names.add(alias.asname or alias.name)
    return names


def _part1_torch_violations(module: ModuleType) -> list[str]:
    """Return the Part 1 function names that use torch (directly or via alias)."""
    try:
        tree = ast.parse(inspect.getsource(module))
    except (OSError, TypeError, SyntaxError):
        return []

    torch_names = _torch_bound_names(tree)
    violations: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name not in _PART1_FN_NAMES:
            continue
        for inner in ast.walk(node):
            uses_alias = isinstance(inner, ast.Name) and inner.id in torch_names
            imports_torch = isinstance(inner, (ast.Import, ast.ImportFrom)) and bool(
                _torch_bound_names(inner)
            )
            if uses_alias or imports_torch:
                violations.append(node.name)
                break
    return violations


# Shortcut callables that would trivialize the Part 2b functions. Maps the
# dotted name (resolved through import aliases) to the function it replaces.
_FORBIDDEN_SHORTCUTS: dict[str, str] = {
    "torch.cdist": "pairwise_distances",
    "torch.nn.functional.cosine_similarity": "cosine_similarity",
    "torch.nn.functional.normalize": "row_normalize",
    "torch.functional.cdist": "pairwise_distances",
}


def _dotted_name(node: ast.AST, alias_roots: dict[str, str]) -> str | None:
    """Resolve an Attribute/Name chain to a dotted name, expanding import aliases."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        root = alias_roots.get(node.id, node.id)
        parts.append(root)
        return ".".join(reversed(parts))
    return None


def _shortcut_violations(module: ModuleType) -> list[str]:
    """Return messages for any forbidden shortcut call used in the module."""
    try:
        tree = ast.parse(inspect.getsource(module))
    except (OSError, TypeError, SyntaxError):
        return []

    # Map local names to the dotted module path they were imported as.
    alias_roots: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                alias_roots[(alias.asname or alias.name).split(".")[0]] = (
                    alias.name if alias.asname else alias.name.split(".")[0]
                )
        elif isinstance(node, ast.ImportFrom) and (node.module or "").startswith("torch"):
            for alias in node.names:
                alias_roots[alias.asname or alias.name] = f"{node.module}.{alias.name}"

    violations: list[str] = []
    for node in ast.walk(tree):
        name = _dotted_name(node, alias_roots)
        if name is None:
            continue
        for forbidden, target in _FORBIDDEN_SHORTCUTS.items():
            if name == forbidden or name.endswith("." + forbidden):
                violations.append(f"{forbidden} (implement {target} yourself instead)")
    return violations


@pytest.fixture(autouse=True)
def set_seed() -> None:
    """Set deterministic seeds for reproducible results."""
    random.seed(42)
    torch.manual_seed(42)
    torch.backends.cudnn.deterministic = True


@pytest.fixture(autouse=True)
def check_no_torch_in_part1(request: pytest.FixtureRequest) -> None:
    """Fail Part 1 (purepython) tests if any Part 1 function uses torch."""
    if "purepython" not in request.node.keywords:
        return
    import linear_algebra as la

    violations = _part1_torch_violations(la)
    if violations:
        pytest.fail(
            f"Part 1 function(s) {', '.join(violations)} use torch (directly, via an "
            "alias, or via `from torch import ...`). Part 1 must be implemented using "
            "only Python built-ins and the math module — no torch, no numpy."
        )


@pytest.fixture(autouse=True)
def check_no_shortcuts(request: pytest.FixtureRequest) -> None:
    """Fail Part 2b (torch) tests if a forbidden shortcut function is used."""
    if "torch" not in request.node.keywords:
        return
    import linear_algebra as la

    violations = _shortcut_violations(la)
    if violations:
        pytest.fail(
            "Forbidden shortcut used: " + "; ".join(sorted(set(violations))) + ". "
            "The point of Part 2b is to build these from the operations you "
            "already wrote."
        )
