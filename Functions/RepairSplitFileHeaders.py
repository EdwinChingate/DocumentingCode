# BundleTools.py
from __future__ import annotations

from called_function_names import *
from insert_internal_imports import *
from top_level_function_defs import *

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================

def RepairSplitFileHeaders(files_dict: Dict[str, str], import_style: str = "star") -> Tuple[Dict[str, str], Dict]:
    func_to_module: Dict[str, str] = {}
    file_to_defs: Dict[str, Set[str]] = {}

    for fname, code in files_dict.items():
        stem = Path(fname).stem
        defs = top_level_function_defs(code or "")
        file_to_defs[fname] = defs
        for d in defs:
            func_to_module[d] = stem

    new_files: Dict[str, str] = {}
    debug = {"imports_added": {}}

    for fname, code in files_dict.items():
        code = code or ""
        stem = Path(fname).stem
        defs_here = file_to_defs.get(fname, set())

        called = called_function_names(code)
        needed_modules: List[str] = []

        for callee in sorted(called):
            if callee in defs_here:
                continue
            mod = func_to_module.get(callee)
            if not mod or mod == stem:
                continue
            needed_modules.append(mod)

        seen = set()
        needed_modules = [m for m in needed_modules if not (m in seen or seen.add(m))]

        fixed = insert_internal_imports(code, needed_modules, import_style=import_style)
        new_files[fname] = fixed
        debug["imports_added"][fname] = needed_modules

    return new_files, debug


# ============================================================
# 4) One-call orchestration: split + repair + write
# ============================================================
