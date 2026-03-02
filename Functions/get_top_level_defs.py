from __future__ import annotations
import ast
# TODO: unresolved names: node

def get_top_level_defs(code: str) -> Set[str]:
    """Returns a set of top-level function and class names defined in the code."""
    try:
        mod = ast.parse(code)
        return {
            node.name for node in mod.body 
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
    except SyntaxError:
        return set()
