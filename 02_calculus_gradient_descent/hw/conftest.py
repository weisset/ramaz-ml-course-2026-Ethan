from __future__ import annotations

import ast
import functools
import random
from pathlib import Path

import pytest
import torch

# Part 1 rule: functions whose names start with this prefix must be pure
# Python arithmetic — no torch, no math library, directly or via helpers.
_MANUAL_PREFIX = "manual_"
_FORBIDDEN_MODULES = frozenset({"torch", "math"})
_MODULE_PATH = Path(__file__).parent / "derivatives.py"


def _forbidden_aliases(tree: ast.Module) -> set[str]:
    """Collect every name bound to torch/math anywhere in the module.

    Catches `import torch`, `import torch as t`, `from torch import tensor`,
    and `from torch import tensor as tt` — at module level or inside functions.
    """
    aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in _FORBIDDEN_MODULES:
                    aliases.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in _FORBIDDEN_MODULES:
                for alias in node.names:
                    aliases.add(alias.asname or alias.name)
    return aliases


def _local_bindings(fn: ast.FunctionDef) -> set[str]:
    """Names bound locally inside fn (args, assignments, loop targets, ...)."""
    names: set[str] = set()
    args = fn.args
    for arg in [*args.posonlyargs, *args.args, *args.kwonlyargs]:
        names.add(arg.arg)
    if args.vararg is not None:
        names.add(args.vararg.arg)
    if args.kwarg is not None:
        names.add(args.kwarg.arg)
    for node in ast.walk(fn):
        targets: list[ast.expr] = []
        if isinstance(node, ast.Assign):
            targets = list(node.targets)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            targets = [node.target]
        elif isinstance(node, ast.For):
            targets = [node.target]
        elif isinstance(node, ast.NamedExpr):
            targets = [node.target]
        elif isinstance(node, ast.comprehension):
            targets = [node.target]
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            targets = [node.optional_vars]
        for target in targets:
            for sub in ast.walk(target):
                if isinstance(sub, ast.Name):
                    names.add(sub.id)
    return names


def _uses_forbidden_directly(fn: ast.FunctionDef, aliases: set[str]) -> bool:
    """True if fn imports torch/math itself or reads a name bound to them."""
    visible_aliases = aliases - _local_bindings(fn)
    for node in ast.walk(fn):
        if isinstance(node, ast.Import):
            if any(a.name.split(".")[0] in _FORBIDDEN_MODULES for a in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in _FORBIDDEN_MODULES:
                return True
        elif (
            isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Load)
            and node.id in visible_aliases
        ):
            return True
    return False


def _called_names(fn: ast.FunctionDef) -> set[str]:
    """Names of plain functions called inside fn (for taint propagation)."""
    names: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            names.add(node.func.id)
    return names


@functools.lru_cache(maxsize=1)
def _tainted_manual_functions() -> tuple[str, ...]:
    """Return manual_* functions that use torch/math, directly or via helpers."""
    try:
        tree = ast.parse(_MODULE_PATH.read_text())
    except (OSError, SyntaxError):
        return ()

    aliases = _forbidden_aliases(tree)
    functions: dict[str, ast.FunctionDef] = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }

    tainted: set[str] = {
        name for name, fn in functions.items() if _uses_forbidden_directly(fn, aliases)
    }
    # Propagate taint through calls (e.g. a manual_* function calling an
    # autograd_* function or a torch-using helper) until a fixed point.
    changed = True
    while changed:
        changed = False
        for name, fn in functions.items():
            if name in tainted:
                continue
            if _called_names(fn) & tainted:
                tainted.add(name)
                changed = True

    return tuple(sorted(name for name in tainted if name.startswith(_MANUAL_PREFIX)))


@pytest.fixture(autouse=True)
def set_seed() -> None:
    """Set deterministic seeds for reproducible results."""
    random.seed(42)
    torch.manual_seed(42)
    torch.backends.cudnn.deterministic = True


# Part 2 rule: the mirror image. autograd_* functions must actually use
# torch.autograd. Without this, every Part 2 class leads with
# test_matches_manual, which compares autograd_* against the student's OWN
# manual_* function, so `return manual_gradient_quadratic(a, b, x_val)` scores
# 45 of 90 raw points with no autograd anywhere.
_AUTOGRAD_PREFIX = "autograd_"

# Attributes and keyword arguments that appear only when autograd is really in
# use. Deliberately broader than just "backward" -- torch.autograd.grad(...) is
# an equally valid route and must not be rejected. Kept terse on purpose: this
# comment is student-visible, so it should not gloss what each marker does.
_AUTOGRAD_MARKERS = frozenset({"backward", "grad", "requires_grad", "requires_grad_"})


def _is_unimplemented(fn: ast.FunctionDef) -> bool:
    """True if fn's body is only a docstring plus a raise (an untouched stub).

    Keeps a fresh stub reporting NotImplementedError instead of a misleading
    "you did not use autograd" message.
    """
    body = [
        node
        for node in fn.body
        if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant))
    ]
    return len(body) == 1 and isinstance(body[0], ast.Raise)


def _shows_autograd_evidence(fn: ast.FunctionDef) -> bool:
    """True if fn mentions any autograd-specific attribute or keyword."""
    for node in ast.walk(fn):
        if isinstance(node, ast.Attribute) and node.attr in _AUTOGRAD_MARKERS:
            return True
        if isinstance(node, ast.keyword) and node.arg in _AUTOGRAD_MARKERS:
            return True
    return False


def _autograd_violations_in(source: str) -> tuple[str, ...]:
    """Return implemented autograd_* functions that do not really use autograd.

    Split out from _autograd_violations so it can be tested against synthetic
    sources without touching derivatives.py.
    """
    tree = ast.parse(source)
    functions: dict[str, ast.FunctionDef] = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }

    # Functions showing real autograd use, propagated through calls so that a
    # student who factors the backward pass into a helper still passes.
    genuine: set[str] = {
        name for name, fn in functions.items() if _shows_autograd_evidence(fn)
    }
    changed = True
    while changed:
        changed = False
        for name, fn in functions.items():
            if name in genuine:
                continue
            if _called_names(fn) & genuine:
                genuine.add(name)
                changed = True

    bad: list[str] = []
    for name, fn in functions.items():
        if not name.startswith(_AUTOGRAD_PREFIX) or _is_unimplemented(fn):
            continue
        delegates = any(
            called.startswith(_MANUAL_PREFIX) for called in _called_names(fn)
        )
        if delegates or name not in genuine:
            bad.append(name)
    return tuple(sorted(bad))


@functools.lru_cache(maxsize=1)
def _autograd_violations() -> tuple[str, ...]:
    try:
        return _autograd_violations_in(_MODULE_PATH.read_text())
    except (OSError, SyntaxError):
        return ()


@pytest.fixture(autouse=True)
def check_autograd_uses_autograd(request: pytest.FixtureRequest) -> None:
    """Fail Part 2 (autograd) tests if any autograd_* function does not use autograd."""
    if "autograd" not in request.node.keywords:
        return
    bad = _autograd_violations()
    if bad:
        pytest.fail(
            f"Part 2 function(s) {', '.join(bad)} do not use torch.autograd. "
            "Mark an input tensor as needing gradients, build f from that "
            "tensor, run the backward pass, and read the gradient off the "
            "input. Calling your Part 1 manual_* function, or redoing the "
            "arithmetic by hand, does not earn Part 2 credit."
        )


@pytest.fixture(autouse=True)
def check_no_forbidden_in_manual(request: pytest.FixtureRequest) -> None:
    """Fail Part 1 (manual) tests if any manual_* function relies on torch or math."""
    if "manual" not in request.node.keywords:
        return
    tainted = _tainted_manual_functions()
    if tainted:
        pytest.fail(
            f"Part 1 function(s) {', '.join(tainted)} use torch or the math "
            "library (directly, through an import alias, or by calling a "
            "function that does). Part 1 must be implemented using only "
            "Python arithmetic — apply the derivative rules directly."
        )
