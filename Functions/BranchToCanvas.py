# BranchToCanvas.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Optional, Set, Tuple, List

import numpy as np
import pandas as pd

from FunctionsIDs import FunctionsIDs
from FillFunctionsMat import FillFunctionsMat
from FunctionsInputs import FunctionsInputs
from FunctionsOutputs import FunctionsOutputs
from GenerateDocFile import GenerateDocFile
from SaveCanvas import SaveCanvas
from TreePositions import TreePositions

from GraphSlice import reachable_from, nodes_on_any_path, expand_tree_from


def _ensure_trailing_slash(p: str) -> str:
    if p and not p.endswith("/"):
        return p + "/"
    return p


def BranchToCanvas(
    FunctionsFolder: str,
    SaveFolder: str,
    OutputCanvasPath: str,
    VaultDocPath: str,
    start_function: str,
    end_function: Optional[str] = None,
    prefix: str = "ms2Topo_",
    max_depth: int = 50,
    node_width: int = 800,
    node_height: int = 600,
    h_gap: int = 200,
    v_gap: int = 400,
    create_missing_docs: bool = True,
    DescriptionsDict: Optional[Dict[str, str]] = None,
) -> Tuple[dict, List[str]]:
    """
    Build a canvas for:
      - all functions reachable from start_function (if end_function is None), OR
      - all functions on any path start_function -> end_function (if end_function provided)

    Also checks docs in SaveFolder and creates missing docs if requested.
    Returns: (CanvasJSON, selected_functions_sorted)
    """
    DescriptionsDict = DescriptionsDict or {}

    FunctionsFolder_p = Path(FunctionsFolder)
    SaveFolder_p = Path(SaveFolder)
    SaveFolder_p.mkdir(parents=True, exist_ok=True)

    # --- Build global matrices (same as FolderToCanvas) ---
    FunctionsListDF = FunctionsIDs(str(FunctionsFolder_p))
    n = len(FunctionsListDF)
    mat = np.zeros((n, n), dtype=int)
    mat = FillFunctionsMat(str(FunctionsFolder_p), mat, FunctionsListDF)

    FunctionsMatDF = pd.DataFrame(
        mat,
        index=FunctionsListDF.index,
        columns=FunctionsListDF.index
    )

    InputsDF = FunctionsInputs(str(FunctionsFolder_p), FunctionsListDF)
    OutputsDF = FunctionsOutputs(str(FunctionsFolder_p), FunctionsListDF)

    # --- Select subgraph ---
    if end_function is None:
        selected: Set[str] = reachable_from(FunctionsMatDF, start_function)
    else:
        selected = nodes_on_any_path(FunctionsMatDF, start_function, end_function)
        # Make sure endpoints are included (they should be, but keep it explicit)
        selected.add(start_function)
        selected.add(end_function)

    selected_list = sorted(selected)

    # Slice matrices so docs list only relationships inside the slice
    SubMatDF = FunctionsMatDF.loc[selected_list, selected_list]
    SubInputsDF = InputsDF.loc[:, selected_list]     # variables x functions
    SubOutputsDF = OutputsDF.loc[:, selected_list]   # variables x functions

    # --- Ensure docs exist (only for selected functions) ---
    DocPaths: Dict[str, str] = {}
    for fn in selected_list:
        save_name = f"{prefix}{fn}"
        file_name = f"{save_name}.md"
        file_path = SaveFolder_p / file_name

        if create_missing_docs and not file_path.exists():
            desc = DescriptionsDict.get(fn, "")
            GenerateDocFile(
                function_name=fn,
                FunctionsMatDF=SubMatDF,
                FunctionsInputsDF=SubInputsDF,
                FunctionsOutputsDF=SubOutputsDF,
                FunctionsFolder=str(FunctionsFolder_p),
                SaveFolder=str(SaveFolder_p),
                prefix=prefix,
                description=desc,
            )

        DocPaths[fn] = file_name

    # --- Build tree + positions ---
    Tree = expand_tree_from(
        SubMatDF,
        start=start_function,
        allowed_nodes=set(selected_list),
        target=end_function,
        max_depth=max_depth,
    )

    Positions = TreePositions(Tree, node_width=node_width, node_height=node_height, h_gap=h_gap, v_gap=v_gap)

    # --- Build Canvas (file nodes) ---
    VaultDocPath = _ensure_trailing_slash(VaultDocPath)

    Nodes = []
    Edges = []

    def process(node):
        node_id = node["id"]
        fn = node["function"]
        x, y = Positions[node_id]

        obsidian_path = VaultDocPath + DocPaths[fn]

        Nodes.append({
            "id": node_id,
            "type": "file",
            "file": obsidian_path,
            "x": int(x),
            "y": int(y),
            "width": node_width,
            "height": node_height
        })

        for child in node["children"]:
            Edges.append({
                "id": f"{node_id}_to_{child['id']}",
                "fromNode": node_id,
                "fromSide": "bottom",
                "toNode": child["id"],
                "toSide": "top"
            })
            process(child)

    for root in Tree:
        process(root)

    Canvas = {"nodes": Nodes, "edges": Edges}
    SaveCanvas(Canvas, OutputCanvasPath)

    return Canvas, selected_list
