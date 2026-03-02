from __future__ import annotations
import re
from typing import List, Tuple


def uncomment_or_prepare_imports(
    code: str,
    needed_modules: List[str]
) -> Tuple[str, List[str]]:
    """
    For each module in needed_modules:
      - If 'from mod import *' already exists  → nothing to do.
      - If '# from mod import *' exists        → uncomment it in-place.
      - Otherwise                              → add mod to the returned remainder list.
    No global variables.
    """
    remaining: List[str] = []

    for mod in needed_modules:
        already_active = re.search(
            rf'^\s*from\s+{re.escape(mod)}\s+import\s+\*\s*$',
            code,
            flags=re.MULTILINE,
        )
        if already_active:
            continue

        commented_pat = re.compile(
            rf'^\s*#\s*from\s+{re.escape(mod)}\s+import\s+\*\s*$',
            flags=re.MULTILINE,
        )
        if commented_pat.search(code):
            code = commented_pat.sub(f'from {mod} import *', code)
        else:
            remaining.append(mod)

    return code, remaining
