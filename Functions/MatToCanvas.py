import hashlib
from TreePositions import *

def MatToCanvas(FunctionsMatDF, node_width=400, node_height=200, h_gap=100, v_gap=400):
    Functions = list(FunctionsMatDF.columns)

    def MakeID(name):
        return hashlib.md5(name.encode()).hexdigest()[:16]

    NodeIDs = {f: MakeID(f) for f in Functions}
    Positions = TreePositions(FunctionsMatDF, node_width, node_height, h_gap, v_gap)

    # --- Build Nodes ---
    Nodes = []
    for f in Functions:
        x, y = Positions[f]
        Nodes.append({
            "id": NodeIDs[f],
            "type": "text",
            "text": "# " + f,
            "x": x,
            "y": y,
            "width": node_width,
            "height": node_height
        })

    # --- Build Edges ---
    Edges = []
    for caller in Functions:
        for callee in Functions:
            if FunctionsMatDF.loc[caller, callee] == 1:
                Edges.append({
                    "id": MakeID(caller + "->" + callee),
                    "fromNode": NodeIDs[caller],
                    "fromSide": "bottom",
                    "toNode": NodeIDs[callee],
                    "toSide": "top"
                })

    Canvas = {"nodes": Nodes, "edges": Edges}
    return Canvas
