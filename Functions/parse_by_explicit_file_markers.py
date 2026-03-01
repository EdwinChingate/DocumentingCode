# BundleTools.py
from __future__ import annotations

from strip_trailing_separators_text import *

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================

EXPLICIT_FILE_MARKER_PATTERNS = [
    re.compile(r'^\s*#\s*---\s*(.+?\.py)\s*---\s*$', re.MULTILINE),
    re.compile(r'^\s*---\s*(.+?\.py)\s*---\s*$', re.MULTILINE),
]

def parse_by_explicit_file_markers(text: str) -> Tuple[Dict[str, str], List[str]]:
    matches = []
    for pat in EXPLICIT_FILE_MARKER_PATTERNS:
        matches.extend(list(pat.finditer(text)))
    matches.sort(key=lambda m: m.start())

    if not matches:
        return {}, ["No explicit '# --- name.py ---' markers found."]

    out: Dict[str, str] = {}

    for i, m in enumerate(matches):
        raw_name = m.group(1).replace("\\", "/").split("/")[-1].strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end]
        content = strip_trailing_separators_text(content.lstrip("\n"))
        out[raw_name] = content

    return out, []
