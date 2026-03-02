import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def inferFunctionName(doc_stem: str, py_stems: set, prefix: Optional[str]) -> Optional[str]:
    if doc_stem in py_stems:
        return doc_stem

    if prefix and doc_stem.startswith(prefix):
        candidate = doc_stem[len(prefix):]
        if candidate in py_stems:
            return candidate

    matches = [s for s in py_stems if doc_stem.endswith(s)]
    return max(matches, key=len) if matches else None
