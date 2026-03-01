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

def infer_filename_from_chunk(chunk: str, idx: int) -> str:
    try:
        mod = ast.parse(chunk)
    except SyntaxError:
        return f"chunk_{idx}.py"

    for node in mod.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            return f"{node.name}.py"
    return f"chunk_{idx}.py"
