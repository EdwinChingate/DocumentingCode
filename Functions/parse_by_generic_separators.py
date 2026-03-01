# BundleTools.py
from __future__ import annotations

from infer_filename_from_chunk import *
from strip_trailing_separators_text import *

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================
GENERIC_CHUNK_SEP = re.compile(r'^\s*#\s*---\s*$', re.MULTILINE)

def parse_by_generic_separators(text: str) -> Tuple[Dict[str, str], List[str]]:
    seps = list(GENERIC_CHUNK_SEP.finditer(text))
    if not seps:
        return {}, ["No generic '# ---' separators found."]

    segments = []
    prev_end = 0
    for m in seps:
        segments.append(text[prev_end:m.start()])
        prev_end = m.end()
    segments.append(text[prev_end:])

    out: Dict[str, str] = {}
    notes: List[str] = []
    chunk_idx = 0

    for seg in segments:
        seg_clean = seg.strip()
        if not seg_clean:
            continue

        chunk_idx += 1
        content = strip_trailing_separators_text(seg.lstrip("\n"))
        fname = infer_filename_from_chunk(content, chunk_idx)

        if fname in out:
            base = fname[:-3]
            k = 2
            while f"{base}_{k}.py" in out:
                k += 1
            fname = f"{base}_{k}.py"
            notes.append(f"Duplicate inferred name; renamed to {fname}")

        out[fname] = content

    return out, notes
