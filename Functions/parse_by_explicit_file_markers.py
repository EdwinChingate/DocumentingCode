from __future__ import annotations
import re
from typing import Dict, List, Tuple

from strip_trailing_separators_text import strip_trailing_separators_text


def parse_by_explicit_file_markers(text: str) -> Tuple[Dict[str, str], List[str]]:
    """
    Split text on '# --- name.py ---' markers.
    All patterns are local — no global variables.
    """
    marker_patterns = [
        re.compile(r'^\s*#\s*---\s*(.+?\.py)\s*---\s*$', re.MULTILINE),
        re.compile(r'^\s*---\s*(.+?\.py)\s*---\s*$',     re.MULTILINE),
    ]

    matches = []
    for pat in marker_patterns:
        matches.extend(pat.finditer(text))
    matches.sort(key=lambda m: m.start())

    if not matches:
        return {}, ["No explicit '# --- name.py ---' markers found."]

    out: Dict[str, str] = {}

    for i, m in enumerate(matches):
        raw_name = m.group(1).replace("\\", "/").split("/")[-1].strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = strip_trailing_separators_text(text[start:end].lstrip("\n"))
        out[raw_name] = content

    return out, []
