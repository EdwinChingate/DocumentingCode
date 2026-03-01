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

def top_level_function_defs(code: str) -> Set[str]:
    try:
        mod = ast.parse(code)
    except SyntaxError:
        return set()
    out = set()
    for node in mod.body:
        if isinstance(node, ast.FunctionDef):
            out.add(node.name)
    return out
