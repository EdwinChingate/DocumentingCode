import hashlib

def ExpandTree(FunctionsMatDF, max_depth=20):
    Functions = list(FunctionsMatDF.columns)

    # Roots: functions not called by anyone
    Roots = [f for f in Functions if FunctionsMatDF[f].sum() == 0]

    Counter = [0]

    def MakeID(name):
        unique = name + '_' + str(Counter[0])
        Counter[0] += 1
        return hashlib.md5(unique.encode()).hexdigest()[:16]

    def BuildBranch(func, depth, Visited):
        NodeID = MakeID(func)
        Children = []

        if depth < max_depth and func not in Visited:
            NewVisited = Visited | {func}
            for callee in Functions:
                if FunctionsMatDF.loc[func, callee] == 1:
                    Child = BuildBranch(callee, depth + 1, NewVisited)
                    Children.append(Child)

        return {
            "function": func,
            "id": NodeID,
            "children": Children
        }

    Tree = [BuildBranch(r, 0, set()) for r in Roots]
    return Tree
