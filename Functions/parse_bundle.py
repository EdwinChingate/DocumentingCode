from __future__ import annotations
from typing import Dict, List, Tuple

from parse_by_explicit_file_markers import parse_by_explicit_file_markers
from parse_by_generic_separators import parse_by_generic_separators
from parse_by_toplevel_defs import parse_by_toplevel_defs


def parse_bundle(text: str) -> Tuple[Dict[str, str], List[str], str]:
    """
    Try three parsing strategies in priority order.
    Returns (files_dict, notes, strategy_name_used).
    No global variables.
    """
    files, notes = parse_by_explicit_file_markers(text)
    if files:
        return files, notes, "explicit_markers"

    files, notes = parse_by_generic_separators(text)
    if files:
        return files, notes, "generic_separators"

    files, notes = parse_by_toplevel_defs(text)
    return files, notes, "toplevel_defs"
