from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Set, Tuple

from called_function_names import called_function_names
from insert_internal_imports import insert_internal_imports
from top_level_function_defs import top_level_function_defs


def RepairSplitFileHeaders(
    files_dict: Dict[str, str],
    import_style: str = "star",
) -> Tuple[Dict[str, str], Dict]:
    """
    For every file in files_dict:
      1. Collect all top-level function definitions across all files.
      2. Find what each file calls.
      3. Insert missing imports for cross-file dependencies.
    No global variables.
    """
    # Pass 1: build func → module map
    func_to_module: Dict[str, str] = {}
    file_to_defs:   Dict[str, Set[str]] = {}

    for fname, code in files_dict.items():
        stem = Path(fname).stem
        defs = top_level_function_defs(code or "")
        file_to_defs[fname] = defs
        for d in defs:
            func_to_module[d] = stem

    # Pass 2: repair each file
    new_files: Dict[str, str] = {}
    debug:     Dict           = {"imports_added": {}}

    for fname, code in files_dict.items():
        code      = code or ""
        stem      = Path(fname).stem
        defs_here = file_to_defs.get(fname, set())

        called = called_function_names(code)

        # only keep external deps that exist in another module
        seen:           Set[str]  = set()
        needed_modules: List[str] = []
        for callee in sorted(called):
            if callee in defs_here:
                continue
            mod = func_to_module.get(callee)
            if not mod or mod == stem:
                continue
            if mod not in seen:
                needed_modules.append(mod)
                seen.add(mod)

        fixed = insert_internal_imports(code, needed_modules, import_style=import_style)
        new_files[fname]                    = fixed
        debug["imports_added"][fname]       = needed_modules

    return new_files, debug
