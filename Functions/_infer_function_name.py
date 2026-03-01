import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def _infer_function_name(doc_stem: str, py_stems: set, prefix: Optional[str]) -> Optional[str]:
    """
    Map a doc stem (e.g. 'ms2Topo_FolderToCanvas') to a .py stem (e.g. 'FolderToCanvas').

    Strategy:
      1) exact match
      2) strip prefix if provided
      3) suffix match against existing py stems (handles unknown prefix)
    """
    # 1) exact match
    if doc_stem in py_stems:
        return doc_stem

    # 2) strip prefix if provided
    if prefix and doc_stem.startswith(prefix):
        candidate = doc_stem[len(prefix):]
        if candidate in py_stems:
            return candidate

    # 3) suffix match: pick the longest py stem that is a suffix of doc_stem
    matches = [s for s in py_stems if doc_stem.endswith(s)]
    if matches:
        return max(matches, key=len)

    return None
