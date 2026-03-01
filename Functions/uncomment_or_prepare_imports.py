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

def uncomment_or_prepare_imports(code: str, needed_modules: List[str]) -> Tuple[str, List[str]]:
    remaining: List[str] = []

    for mod in needed_modules:
        if re.search(rf'^\s*from\s+{re.escape(mod)}\s+import\s+\*\s*$', code, flags=re.MULTILINE):
            continue

        commented_pat = re.compile(
            rf'^\s*#\s*from\s+{re.escape(mod)}\s+import\s+\*\s*$',
            flags=re.MULTILINE
        )

        if commented_pat.search(code):
            code = commented_pat.sub(f'from {mod} import *', code)
        else:
            remaining.append(mod)

    return code, remaining
