import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


_FILE_MARKER_PATTERNS = [
    re.compile(r'^\s*#\s*---\s*(.+?\.py)\s*---\s*$'),    # "# --- Name.py ---"
    re.compile(r'^\s*---\s*(.+?\.py)\s*---\s*$'),        # "--- /path/Name.py ---"
]

_SEPARATOR_PAT = re.compile(r'^\s*#\s*#{20,}\s*$')        # lines like "###########..."


def _strip_trailing_separators(lines: List[str]) -> List[str]:
    """Remove trailing separator blocks like long hash lines + surrounding blanks."""
    i = len(lines)
    while i > 0 and (lines[i-1].strip() == "" or _SEPARATOR_PAT.match(lines[i-1]) is not None):
        i -= 1
    return lines[:i]
