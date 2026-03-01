# GraphSlice.py
from __future__ import annotations
from collections import deque
import hashlib
from typing import Iterable, Optional, Set, List, Dict

import pandas as pd


def reachable_from(mat: pd.DataFrame, start: str) -> Set[str]:
    """
    Return all nodes reachable from `start` following edges start -> callee.
    mat is adjacency with rows=caller, cols=callee, values 0/1.
    """
    if start not in mat.index:
        raise KeyError(f"start function '{start}' not found in adjacency matrix")

    visited: Set[str] = set()
    q = deque([start])

    while q:
        u = q.popleft()
        if u in visited:
            continue
        visited.add(u)

        # neighbors: callees of u
        neigh = mat.columns[mat.loc[u].astype(int) == 1].tolist()
        for v in neigh:
            if v not in visited:
                q.append(v)

    return visited


def reachable_to(mat: pd.DataFrame, target: str) -> Set[str]:
    """
    Return all nodes that can reach `target` (i.e. ancestors of target).
    Equivalent to reachable_from(mat.T, target) but keeps naming explicit.
    """
    if target not in mat.columns:
        raise KeyError(f"target function '{target}' not found in adjacency matrix")
    return reachable_from(mat.T, target)


def nodes_on_any_path(mat: pd.DataFrame, start: str, target: str) -> Set[str]:
    """
    Nodes that lie on at least one directed path start -> ... -> target.

    Trick: node is on some start->target path iff:
        node is reachable from start  AND  target is reachable from node
    So we intersect descendants(start) with ancestors(target).
    """
    desc = reachable_from(mat, start)
    anc = reachable_to(mat, target)
    return desc.intersection(anc)


def expand_tree_from(
    mat: pd.DataFrame,
    start: str,
    allowed_nodes: Optional[Set[str]] = None,
    target: Optional[str] = None,
    max_depth: int = 50,
) -> List[Dict]:
    """
    Build a *tree-shaped* expansion from start using mat adjacency.
    This is a "tree view" of a directed graph; nodes may repeat if there
    are multiple paths (common in dependency graphs).

    - allowed_nodes: if given, only include/expand within this set
    - target: if given, stop expanding once target is reached (still included)
    """
    if start not in mat.index:
        raise KeyError(f"start function '{start}' not found in adjacency matrix")

    counter = [0]

    def make_id(name: str) -> str:
        unique = f"{name}_{counter[0]}"
        counter[0] += 1
        return hashlib.md5(unique.encode()).hexdigest()[:16]

    def build(node_func: str, depth: int, visited_path: Set[str]) -> Dict:
        node_id = make_id(node_func)
        children = []

        if target is not None and node_func == target:
            return {"function": node_func, "id": node_id, "children": []}

        if depth >= max_depth:
            return {"function": node_func, "id": node_id, "children": []}

        # prevent infinite recursion on cycles along this branch
        if node_func in visited_path:
            return {"function": node_func, "id": node_id, "children": []}

        # expand callees
        callees = mat.columns[mat.loc[node_func].astype(int) == 1].tolist()
        for callee in callees:
            if allowed_nodes is not None and callee not in allowed_nodes:
                continue
            child = build(callee, depth + 1, visited_path | {node_func})
            children.append(child)

        return {"function": node_func, "id": node_id, "children": children}

    return [build(start, 0, set())]
