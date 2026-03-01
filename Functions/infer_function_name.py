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

def infer_function_name(doc_stem: str, py_stems: set[str], prefix: Optional[str]) -> Optional[str]:
    if doc_stem in py_stems:
        return doc_stem

    if prefix and doc_stem.startswith(prefix):
        candidate = doc_stem[len(prefix):]
        if candidate in py_stems:
            return candidate

    matches = [s for s in py_stems if doc_stem.endswith(s)]
    return max(matches, key=len) if matches else None
