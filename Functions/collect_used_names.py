# --- collect_used_names.py ---
from __future__ import annotations
import ast
import builtins
from typing import Set, Tuple


def get_builtin_names() -> Set[str]:
    return set(dir(builtins)) | {
        "Dict", "List", "Set", "Tuple", "Optional", "Any",
        "Union", "Callable", "Iterator", "Generator",
        "Type", "ClassVar", "Final", "Literal",
        "True", "False", "None",
    }


def get_root_name(node: ast.expr) -> str | None:
    """Walk an attribute chain and return the root Name string, or None."""
    while isinstance(node, ast.Attribute):
        node = node.value
    if isinstance(node, ast.Name):
        return node.id
    return None


def get_assigned_names(node: ast.AST, out_set: Set[str]) -> None:
    """Recursively extracts names from assignments, handling tuple/list unpacking."""
    if isinstance(node, ast.Name):
        out_set.add(node.id)
    elif isinstance(node, (ast.Tuple, ast.List)):
        for elt in node.elts:
            get_assigned_names(elt, out_set)
    elif isinstance(node, ast.Starred):
        get_assigned_names(node.value, out_set)


def visit_node(
    node           : ast.AST,
    direct_calls   : Set[str],
    root_names     : Set[str],
    all_names      : Set[str],
    locally_defined: Set[str],
) -> None:
    """
    Recursive AST visitor — no class needed.
    Populates the four sets in place.
    """
    # ── definitions ──────────────────────────────────────────────────────
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        locally_defined.add(node.name)
        for arg in (
            node.args.args
            + node.args.posonlyargs
            + node.args.kwonlyargs
        ):
            locally_defined.add(arg.arg)
        if node.args.vararg:
            locally_defined.add(node.args.vararg.arg)
        if node.args.kwarg:
            locally_defined.add(node.args.kwarg.arg)

    elif isinstance(node, ast.ClassDef):
        locally_defined.add(node.name)

    elif isinstance(node, ast.Assign):
        for target in node.targets:
            get_assigned_names(target, locally_defined)

    elif isinstance(node, ast.AnnAssign):
        get_assigned_names(node.target, locally_defined)

    elif isinstance(node, ast.For):
        get_assigned_names(node.target, locally_defined)

    elif isinstance(node, ast.ExceptHandler):
        if node.name:
            locally_defined.add(node.name)

    elif isinstance(node, ast.With):
        for item in node.items:
            if item.optional_vars is not None:
                get_assigned_names(item.optional_vars, locally_defined)

    # ── imports: mark as locally defined, never as "used" ────────────────
    elif isinstance(node, ast.Import):
        for alias in node.names:
            locally_defined.add(alias.asname or alias.name.split(".")[0])

    elif isinstance(node, ast.ImportFrom):
        for alias in node.names:
            if alias.name != "*":
                locally_defined.add(alias.asname or alias.name)

    # ── usages ───────────────────────────────────────────────────────────
    # Only capture names that are actively being used/read (Load context)
    elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
        all_names.add(node.id)

    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            direct_calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            root = get_root_name(node.func.value)
            if root:
                root_names.add(root)

    elif isinstance(node, ast.Attribute):
        root = get_root_name(node.value)
        if root:
            root_names.add(root)

    # ── recurse ───────────────────────────────────────────────────────────
    for child in ast.iter_child_nodes(node):
        visit_node(child, direct_calls, root_names, all_names, locally_defined)


def collect_used_names(source: str) -> Tuple[Set[str], Set[str], Set[str], Set[str]]:
    """
    Single AST pass over source code.
    Returns (direct_calls, root_names, all_names, locally_defined).
    """
    builtin_names = get_builtin_names()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set(), set(), set(), set()

    direct_calls:    Set[str] = set()
    root_names:      Set[str] = set()
    all_names:       Set[str] = set()
    locally_defined: Set[str] = set()

    visit_node(tree, direct_calls, root_names, all_names, locally_defined)

    direct_calls    -= builtin_names
    root_names      -= builtin_names
    all_names       -= builtin_names

    return direct_calls, root_names, all_names, locally_defined
