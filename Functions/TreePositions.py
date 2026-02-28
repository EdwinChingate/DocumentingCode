def TreePositions(Tree, node_width=400, node_height=200, h_gap=100, v_gap=400):
    Positions = {}

    def GetWidth(node):
        Kids = node["children"]
        if not Kids:
            return node_width
        return sum(GetWidth(c) for c in Kids) + h_gap * (len(Kids) - 1)

    def PlaceNode(node, x, y):
        Positions[node["id"]] = (int(x), int(y))
        Kids = node["children"]
        if not Kids:
            return
        TotalW = sum(GetWidth(c) for c in Kids) + h_gap * (len(Kids) - 1)
        StartX = x + node_width / 2 - TotalW / 2
        CurrX = StartX
        for child in Kids:
            ChildW = GetWidth(child)
            ChildX = CurrX + ChildW / 2 - node_width / 2
            PlaceNode(child, ChildX, y + node_height + v_gap)
            CurrX += ChildW + h_gap

    # Place root trees side by side
    TotalRootW = sum(GetWidth(r) for r in Tree) + h_gap * max(len(Tree) - 1, 0)
    CurrX = -TotalRootW / 2
    for root in Tree:
        RootW = GetWidth(root)
        RootX = CurrX + RootW / 2 - node_width / 2
        PlaceNode(root, RootX, 0)
        CurrX += RootW + h_gap

    return Positions
