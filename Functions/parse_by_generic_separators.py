from __future__ import annotations
import re
from typing import Dict, List, Tuple

from infer_filename_from_chunk import infer_filename_from_chunk
from strip_trailing_separators_text import strip_trailing_separators_text


def parse_by_generic_separators(text: str) -> Tuple[Dict[str, str], List[str]]:
    """
    Split text on '# ---' separators.
    Pattern is local — no global variables.
    """
    generic_chunk_sep = re.compile(r'^\s*#\s*---\s*$', re.MULTILINE)

    seps = list(generic_chunk_sep.finditer(text))
    if not seps:
        return {}, ["No generic '# ---' separators found."]

    segments: List[str] = []
    prev_end = 0
    for m in seps:
        segments.append(text[prev_end : m.start()])
        prev_end = m.end()
    segments.append(text[prev_end:])

    out: Dict[str, str] = {}
    notes: List[str] = []
    chunk_idx = 0

    for seg in segments:
        if not seg.strip():
            continue

        chunk_idx += 1
        content = strip_trailing_separators_text(seg.lstrip("\n"))
        fname = infer_filename_from_chunk(content, chunk_idx)

        if fname in out:
            base = fname[:-3]
            k = 2
            while f"{base}_{k}.py" in out:
                k += 1
            fname = f"{base}_{k}.py"
            notes.append(f"Duplicate inferred name; renamed to {fname}")

        out[fname] = content

    return out, notes
