# BundleTools.py
from __future__ import annotations

from parse_by_explicit_file_markers import *
from parse_by_generic_separators import *
from parse_by_toplevel_defs import *

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================

def parse_bundle(text: str) -> Tuple[Dict[str, str], List[str], str]:
    files, notes = parse_by_explicit_file_markers(text)
    if files:
        return files, notes, "explicit_markers"

    files, notes2 = parse_by_generic_separators(text)
    if files:
        return files, notes2, "generic_separators"

    files, notes3 = parse_by_toplevel_defs(text)
    return files, notes3, "toplevel_defs"


# ============================================================
# 3) Header repair: uncomment "#from X import *" if needed + insert missing
# ============================================================

IMPORT_LINE_PAT = re.compile(r"^\s*(from\s+([A-Za-z_]\w*)\s+import|import\s+([A-Za-z_]\w*))")
