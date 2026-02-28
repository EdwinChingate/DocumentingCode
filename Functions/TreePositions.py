def TreePositions(FunctionsMatDF, node_width=400, node_height=200, h_gap=100, v_gap=400):
    Functions = list(FunctionsMatDF.columns)
    N = len(Functions)

    # --- Assign depth (max distance from roots, handles DAGs) ---
    Depth = {f: 0 for f in Functions}
    for i in range(N):  # cycle protection
        Changed = False
        for caller in Functions:
            for callee in Functions:
                if FunctionsMatDF.loc[caller, callee] == 1:
                    NewDepth = Depth[caller] + 1
                    if NewDepth > Depth[callee]:
                        Depth[callee] = NewDepth
                        Changed = True
        if not Changed:
            break

    # --- Build children map (direct parent→child by depth) ---
    Children = {f: [] for f in Functions}
    for caller in Functions:
        for callee in Functions:
            if FunctionsMatDF.loc[caller, callee] == 1:
                if Depth[callee] == Depth[caller] + 1:
                    Children[caller].append(callee)

    # --- Compute subtree widths (for centering) ---
    SubWidth = {}
    def GetWidth(node):
        if node in SubWidth:
            return SubWidth[node]
        kids = Children[node]
        if not kids:
            SubWidth[node] = node_width
        else:
            SubWidth[node] = sum(GetWidth(c) for c in kids) + h_gap * (len(kids) - 1)
        return SubWidth[node]

    for f in Functions:
        GetWidth(f)

    # --- Assign positions top-down ---
    Positions = {}
    def PlaceNode(node, x, y):
        Positions[node] = (int(x), int(y))
        kids = Children[node]
        if not kids:
            return
        TotalW = sum(SubWidth[c] for c in kids) + h_gap * (len(kids) - 1)
        StartX = x + node_width / 2 - TotalW / 2
        CurrX = StartX
        for child in kids:
            ChildX = CurrX + SubWidth[child] / 2 - node_width / 2
            PlaceNode(child, ChildX, y + node_height + v_gap)
            CurrX += SubWidth[child] + h_gap

    # --- Place root trees side by side ---
    Roots = [f for f in Functions if Depth[f] == 0]
    TotalRootW = sum(SubWidth[r] for r in Roots) + h_gap * max(len(Roots) - 1, 0)
    CurrX = -TotalRootW / 2
    for root in Roots:
        RootX = CurrX + SubWidth[root] / 2 - node_width / 2
        PlaceNode(root, RootX, 0)
        CurrX += SubWidth[root] + h_gap

    return Positions
