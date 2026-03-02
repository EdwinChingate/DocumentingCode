from __future__ import annotations
import re
from typing import Set


def existing_import_modules(code: str) -> Set[str]:
    """
    Return module names already imported in code.
    Pattern is defined locally — no global variables.
    """
    import_line_pat = re.compile(
        r"^\s*(from\s+([A-Za-z_]\w*)\s+import|import\s+([A-Za-z_]\w*))"
    )

    mods: Set[str] = set()
    for line in code.splitlines():
        m = import_line_pat.match(line)
        if not m:
            continue
        if m.group(2):
            mods.add(m.group(2))
        if m.group(3):
            mods.add(m.group(3))
    return mods
