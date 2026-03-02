from functionsFromCanvasWithPositions import *

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def commentInternalStarImports(code: str, bundle_function_names: List[str]) -> str:
    pattern = re.compile(
        r'^\s*from\s+([A-Za-z_]\w*)\s+import\s+\*\s*$',
        re.MULTILINE
    )

    def replacer(match):
        module = match.group(1)
        if module in bundle_function_names:
            return f"#from {module} import *"
        return match.group(0)

    return pattern.sub(replacer, code)


def CanvasToCombinedTxt(
    canvas_path: str | Path,
    functions_folder: str | Path,
    output_txt_path: str | Path,
    prefix: Optional[str] = None,
    allow_text_nodes: bool = True,
    gap_lines: int = 4,
) -> Dict:

    canvas_path = Path(canvas_path)
    functions_folder = Path(functions_folder)
    output_txt_path = Path(output_txt_path)
    output_txt_path.parent.mkdir(parents=True, exist_ok=True)

    if not canvas_path.exists():
        raise FileNotFoundError(f"Canvas not found: {canvas_path}")
    if not functions_folder.exists():
        raise FileNotFoundError(f"Functions folder not found: {functions_folder}")

    functions, debug, _ = functionsFromCanvasWithPositions(
        canvas_path=canvas_path,
        functions_folder=functions_folder,
        prefix=prefix,
        allow_text_nodes=allow_text_nodes,
    )

    included: List[str] = []
    missing: List[str] = []

    gap = "\n" * (gap_lines + 1)

    chunks: List[str] = []

    chunks.append(f"# Combined export from canvas: {canvas_path.name}\n")
    chunks.append(f"# Functions folder: {functions_folder}\n")
    chunks.append(f"# Functions included (detected in canvas): {len(functions)}\n")

    if debug.get("unresolved_candidates"):
        chunks.append(f"# Unresolved canvas references: {len(debug['unresolved_candidates'])}\n")
        for u in debug["unresolved_candidates"]:
            chunks.append(f"#   - {u}\n")

    chunks.append(gap)

    for fn in functions:
        py_path = functions_folder / f"{fn}.py"

        if not py_path.exists():
            missing.append(fn)
            continue

        code = py_path.read_text(encoding="utf-8", errors="replace")

        # Comment internal imports
        code = commentInternalStarImports(code, functions)

        included.append(fn)

        chunks.append(f"# --- {fn}.py ---\n")
        chunks.append(code.rstrip() + "\n")
        chunks.append(gap)

    final_text = "".join(chunks).rstrip() + "\n"
    output_txt_path.write_text(final_text, encoding="utf-8")

    return {
        "output_txt_path": str(output_txt_path),
        "included": included,
        "missing": missing,
        **debug,
    }
