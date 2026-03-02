from __future__ import annotations

# TODO: could not auto-resolve the following names —
#   from ??? import node



def top_level_function_defs(code: str) -> Set[str]:
    """
    Return the set of top-level function and class names defined in code.
    No global variables, no classes.
    """
    try:
        mod = ast.parse(code)
    except SyntaxError:
        return set()

    return {
        node.name
        for node in mod.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
