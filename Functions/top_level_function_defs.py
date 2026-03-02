from __future__ import annotations
import ast
from typing import Set


def top_level_function_defs(code: str) -> Set[str]:
    """
    Return the set of top-level function names defined in code.
    No global variables.
    """
    try:
        mod = ast.parse(code)
    except SyntaxError:
        return set()

    return {
        node.name
        for node in mod.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
