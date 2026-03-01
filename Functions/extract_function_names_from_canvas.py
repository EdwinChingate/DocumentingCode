# BundleTools.py
from __future__ import annotations

from extract_stem_from_canvas_file_field import *
from infer_function_name import *

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================

def extract_function_names_from_canvas(
    canvas_path: str | Path,
    functions_folder: str | Path,
    prefix: Optional[str] = None,
    allow_text_nodes: bool = True,
    order: str = "canvas",  # "canvas" (y,x), "alpha"
) -> Tuple[List[str], Dict]:
    canvas_path = Path(canvas_path)
    functions_folder = Path(functions_folder)

    if not canvas_path.exists():
        raise FileNotFoundError(f"Canvas not found: {canvas_path}")
    if not functions_folder.exists():
        raise FileNotFoundError(f"Functions folder not found: {functions_folder}")

    py_stems = {p.stem for p in functions_folder.glob("*.py")}

    data = json.loads(canvas_path.read_text(encoding="utf-8"))
    nodes = data.get("nodes", [])

    extracted: List[Tuple[str, float, float, str]] = []  # (fn, y, x, source)

    for n in nodes:
        ntype = n.get("type", "")
        x = float(n.get("x", 0))
        y = float(n.get("y", 0))

        if ntype == "file" and "file" in n:
            doc_stem = extract_stem_from_canvas_file_field(n["file"])
            fn = infer_function_name(doc_stem, py_stems, prefix)
            if fn:
                extracted.append((fn, y, x, "file"))
            else:
                extracted.append((f"__UNRESOLVED__:{doc_stem}", y, x, "file-unresolved"))
            continue

        if allow_text_nodes and ntype == "text" and "text" in n:
            text = str(n["text"]).strip()
            first_line = text.splitlines()[0].strip() if text else ""
            if first_line.startswith("#"):
                candidate = first_line.lstrip("#").strip()
                if candidate in py_stems:
                    extracted.append((candidate, y, x, "text"))
                else:
                    extracted.append((f"__UNRESOLVED__:{candidate}", y, x, "text-unresolved"))

    if order == "alpha":
        extracted.sort(key=lambda t: t[0])
    else:
        extracted.sort(key=lambda t: (t[1], t[2], t[0]))

    seen = set()
    function_names = []
    unresolved = []

    for fn, _, _, _ in extracted:
        if fn.startswith("__UNRESOLVED__:"):
            unresolved.append(fn.replace("__UNRESOLVED__:", ""))
            continue
        if fn not in seen:
            seen.add(fn)
            function_names.append(fn)

    debug = {
        "n_nodes": len(nodes),
        "n_py_files_in_folder": len(py_stems),
        "n_functions_extracted": len(function_names),
        "unresolved_candidates": unresolved,
    }
    return function_names, debug
