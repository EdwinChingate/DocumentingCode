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

def strip_trailing_separators_text(s: str) -> str:
    lines = s.splitlines()
    i = len(lines)
    while i > 0:
        line = lines[i - 1].strip()
        if line == "" or SEPARATOR_HASHLINE.match(lines[i - 1]):
            i -= 1
        else:
            break
    return "\n".join(lines[:i]).rstrip() + ("\n" if i > 0 else "")
