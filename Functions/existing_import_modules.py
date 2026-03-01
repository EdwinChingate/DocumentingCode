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

IMPORT_LINE_PAT = re.compile(r"^\s*(from\s+([A-Za-z_]\w*)\s+import|import\s+([A-Za-z_]\w*))")

def existing_import_modules(code: str) -> Set[str]:
    mods = set()
    for line in code.splitlines():
        m = IMPORT_LINE_PAT.match(line)
        if not m:
            continue
        if m.group(2):
            mods.add(m.group(2))
        if m.group(3):
            mods.add(m.group(3))
    return mods


class CallNameCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.called: Set[str] = set()

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self.called.add(node.func.id)
        self.generic_visit(node)
