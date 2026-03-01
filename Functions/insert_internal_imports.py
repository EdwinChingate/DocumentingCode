# BundleTools.py
from __future__ import annotations

from existing_import_modules import *
from module_insertion_index_for_imports import *
from uncomment_or_prepare_imports import *

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================

def insert_internal_imports(code: str, needed_modules: List[str], import_style: str = "star") -> str:
    if not needed_modules:
        return code

    code, needed_modules = uncomment_or_prepare_imports(code, needed_modules)
    if not needed_modules:
        return code

    existing = existing_import_modules(code)

    import_lines: List[str] = []
    for mod in needed_modules:
        if mod in existing:
            continue
        if import_style == "name":
            import_lines.append(f"from {mod} import {mod}\n")
        else:
            import_lines.append(f"from {mod} import *\n")

    if not import_lines:
        return code

    lines = code.splitlines(keepends=True)
    insert_idx = module_insertion_index_for_imports(code)

    block: List[str] = []
    if insert_idx > 0 and lines[insert_idx - 1].strip() != "":
        block.append("\n")
    block.extend(import_lines)
    if insert_idx < len(lines) and (insert_idx == 0 or lines[insert_idx].strip() != ""):
        block.append("\n")

    new_lines = lines[:insert_idx] + block + lines[insert_idx:]
    return "".join(new_lines)
