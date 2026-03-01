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
TOPLEVEL_DEF_PAT = re.compile(r'^(?:async\s+def|def)\s+([A-Za-z_]\w*)\s*\(', re.MULTILINE)

def parse_by_toplevel_defs(text: str, include_header_imports: bool = True) -> Tuple[Dict[str, str], List[str]]:
    matches = list(TOPLEVEL_DEF_PAT.finditer(text))
    if not matches:
        return {}, ["No top-level 'def name(' blocks found."]

    header = text[:matches[0].start()] if include_header_imports else ""
    out: Dict[str, str] = {}

    for i, m in enumerate(matches):
        name = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].rstrip() + "\n"
        out[f"{name}.py"] = (header + body) if include_header_imports else body

    return out, []
