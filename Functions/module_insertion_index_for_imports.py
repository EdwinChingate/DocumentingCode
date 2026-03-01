# BundleTools.py
from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================

def module_insertion_index_for_imports(code: str) -> int:
    lines = code.splitlines(keepends=True)
    try:
        mod = ast.parse(code)
    except SyntaxError:
        return 0

    doc_end = 0
    future_end = 0

    if mod.body:
        first = mod.body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(getattr(first, "value", None), ast.Constant)
            and isinstance(first.value.value, str)
        ):
            doc_end = getattr(first, "end_lineno", first.lineno) or 0

    for node in mod.body:
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            future_end = max(future_end, getattr(node, "end_lineno", node.lineno) or 0)

    insert_after_1based = max(doc_end, future_end)
    return min(max(insert_after_1based, 0), len(lines))
