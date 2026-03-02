from __future__ import annotations
import ast
from typing import Set


def called_function_names(code: str) -> Set[str]:
    """
    Return the set of all function/callable names that appear in Call nodes.
    No global variables.
    """
    class _CallNameCollector(ast.NodeVisitor):
        def __init__(self) -> None:
            self.called: Set[str] = set()

        def visit_Call(self, node: ast.Call) -> None:
            if isinstance(node.func, ast.Name):
                self.called.add(node.func.id)
            self.generic_visit(node)

    try:
        mod = ast.parse(code)
    except SyntaxError:
        return set()

    collector = _CallNameCollector()
    collector.visit(mod)
    return collector.called
