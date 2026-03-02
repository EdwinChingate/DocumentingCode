from extractStemFromCanvasFileField import *
from inferFunctionName import *

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def functionsFromCanvasWithPositions(
    canvas_path: Path,
    functions_folder: Path,
    prefix: Optional[str],
    allow_text_nodes: bool,
) -> Tuple[List[str], Dict, Dict[str, Tuple[float, float]]]:
    """
    Returns:
      - functions list (reverse canvas order: deepest → root)
      - debug dict
      - position dict {fn: (max_y, max_x)}
    """
    py_stems = {p.stem for p in functions_folder.glob("*.py")}
    data = json.loads(canvas_path.read_text(encoding="utf-8"))
    nodes = data.get("nodes", [])

    occurrences: List[Tuple[str, float, float]] = []
    unresolved: List[str] = []

    for n in nodes:
        ntype = n.get("type", "")
        x = float(n.get("x", 0))
        y = float(n.get("y", 0))

        if ntype == "file" and "file" in n:
            doc_stem = extractStemFromCanvasFileField(n["file"])
            fn = inferFunctionName(doc_stem, py_stems, prefix)
            if fn:
                occurrences.append((fn, y, x))
            else:
                unresolved.append(doc_stem)
            continue

        if allow_text_nodes and ntype == "text" and "text" in n:
            text = str(n["text"]).strip()
            first_line = text.splitlines()[0].strip() if text else ""
            if first_line.startswith("#"):
                candidate = first_line.lstrip("#").strip()
                if candidate in py_stems:
                    occurrences.append((candidate, y, x))
                else:
                    unresolved.append(candidate)

    position: Dict[str, Tuple[float, float]] = {}

    for fn, y, x in occurrences:
        if fn not in position:
            position[fn] = (y, x)
        else:
            by, bx = position[fn]
            if (y > by) or (y == by and x > bx):
                position[fn] = (y, x)

    # Deepest first → highest y first
    functions_sorted = sorted(
        position.keys(),
        key=lambda fn: (position[fn][0], position[fn][1]),
        reverse=True,
    )

    debug = {
        "n_nodes": len(nodes),
        "n_py_files_in_folder": len(py_stems),
        "n_functions_extracted": len(functions_sorted),
        "unresolved_candidates": unresolved,
    }

    return functions_sorted, debug, position
