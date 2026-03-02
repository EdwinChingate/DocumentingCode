from __future__ import annotations
import ast


def infer_filename_from_chunk(chunk: str, idx: int) -> str:
    """
    Guess a filename from the first def/class found in chunk.
    Falls back to chunk_<idx>.py if nothing is found or chunk is unparseable.
    """
    try:
        mod = ast.parse(chunk)
    except SyntaxError:
        return f"chunk_{idx}.py"

    for node in mod.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return f"{node.name}.py"

    return f"chunk_{idx}.py"
