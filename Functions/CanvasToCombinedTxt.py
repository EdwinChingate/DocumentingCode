# BundleTools.py
from __future__ import annotations

from extract_function_names_from_canvas import *

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================

def CanvasToCombinedTxt(
    canvas_path: str | Path,
    functions_folder: str | Path,
    output_txt_path: str | Path,
    prefix: Optional[str] = None,
    allow_text_nodes: bool = True,
    order: str = "canvas",  # "canvas" or "alpha"
    separator: str = "\n\n" + ("#" * 80) + "\n\n",
) -> Dict:
    """
    Read function names from a canvas, load corresponding .py files from functions_folder,
    and concatenate them into one output txt file.

    Returns a summary dict with included/missing/unresolved info.
    """
    canvas_path = Path(canvas_path)
    functions_folder = Path(functions_folder)
    output_txt_path = Path(output_txt_path)
    output_txt_path.parent.mkdir(parents=True, exist_ok=True)

    functions, debug = extract_function_names_from_canvas(
        canvas_path=canvas_path,
        functions_folder=functions_folder,
        prefix=prefix,
        allow_text_nodes=allow_text_nodes,
        order=order,
    )

    included = []
    missing = []

    chunks = []
    chunks.append(f"# Combined export from canvas: {canvas_path.name}\n")
    chunks.append(f"# Functions folder: {functions_folder}\n")
    chunks.append(f"# Functions included: {len(functions)}\n")

    if debug.get("unresolved_candidates"):
        chunks.append(f"# Unresolved canvas references (could not map to .py): {len(debug['unresolved_candidates'])}\n")
        for u in debug["unresolved_candidates"]:
            chunks.append(f"#   - {u}\n")

    chunks.append(separator)

    for fn in functions:
        py_path = functions_folder / f"{fn}.py"
        if not py_path.exists():
            missing.append(fn)
            continue

        code = py_path.read_text(encoding="utf-8", errors="replace")
        included.append(fn)

        chunks.append(f"# --- {fn}.py ---\n")
        chunks.append(code.rstrip() + "\n")
        chunks.append(separator)

    output_txt_path.write_text("".join(chunks), encoding="utf-8")

    return {
        "output_txt_path": str(output_txt_path),
        "included": included,
        "missing": missing,
        **debug,
    }
