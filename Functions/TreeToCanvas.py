from ExpandTree import *
from TreePositions import *

def TreeToCanvas(FunctionsMatDF, DocPaths, VaultDocPath, node_width=800, node_height=600, h_gap=200, v_gap=400):
    Tree = ExpandTree(FunctionsMatDF)
    Positions = TreePositions(Tree, node_width, node_height, h_gap, v_gap)

    Nodes = []
    Edges = []
    
    # Ensure the VaultDocPath ends with a slash if it isn't empty
    if VaultDocPath and not VaultDocPath.endswith('/'):
        VaultDocPath += '/'

    def ProcessNode(node):
        x, y = Positions[node["id"]]
        func_name = node["function"]
        
        # Combine the target Vault path with the filename
        ObsidianInternalPath = VaultDocPath + DocPaths[func_name]
        
        Nodes.append({
            "id": node["id"],
            "type": "file",
            "file": ObsidianInternalPath, 
            "x": x,
            "y": y,
            "width": node_width,
            "height": node_height
        })
        
        for child in node["children"]:
            Edges.append({
                "id": node["id"] + "_to_" + child["id"],
                "fromNode": node["id"],
                "fromSide": "bottom",
                "toNode": child["id"],
                "toSide": "top"
            })
            ProcessNode(child)

    for root in Tree:
        ProcessNode(root)

    Canvas = {"nodes": Nodes, "edges": Edges}
    return Canvas
