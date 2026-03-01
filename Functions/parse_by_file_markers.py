from _strip_trailing_separators import *

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


_FILE_MARKER_PATTERNS = [
    re.compile(r'^\s*#\s*---\s*(.+?\.py)\s*---\s*$'),    # "# --- Name.py ---"
    re.compile(r'^\s*---\s*(.+?\.py)\s*---\s*$'),        # "--- /path/Name.py ---"
]

_SEPARATOR_PAT = re.compile(r'^\s*#\s*#{20,}\s*$')        # lines like "###########..."


def _parse_by_file_markers(text: str) -> Tuple[Dict[str, str], List[str]]:
    """
    Parse bundle where file boundaries are explicitly marked.
    Returns (files_dict, unresolved_markers).
    """
    lines = text.splitlines(keepends=True)

    current_name: Optional[str] = None
    current_buf: List[str] = []
    out: Dict[str, List[str]] = {}
    unresolved: List[str] = []

    def flush():
        nonlocal current_name, current_buf
        if current_name is None:
            return
        buf = _strip_trailing_separators(current_buf)
        if buf:
            out.setdefault(current_name, []).extend(buf)
        current_name = None
        current_buf = []

    for line in lines:
        marker_name = None
        for pat in _FILE_MARKER_PATTERNS:
            m = pat.match(line)
            if m:
                marker_name = m.group(1).replace("\\", "/").split("/")[-1]  # basename
                break

        if marker_name:
            flush()
            current_name = marker_name
            current_buf = []
            continue

        if current_name is None:
            # preamble before first marker -> ignore, but keep track if you want
            continue

        current_buf.append(line)

    flush()

    # Convert list-of-lines into string
    files_dict = {name: "".join(buf) for name, buf in out.items()}

    if not files_dict:
        unresolved.append("No file markers found.")

    return files_dict, unresolved


_TOPLEVEL_DEF_PAT = re.compile(r'^(def)\s+([A-Za-z_]\w*)\s*\(', re.MULTILINE)
