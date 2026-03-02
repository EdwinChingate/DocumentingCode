from __future__ import annotations
import re
from typing import Dict, List, Tuple


def parse_by_toplevel_defs(
    text: str,
    include_header_imports: bool = True,
) -> Tuple[Dict[str, str], List[str]]:
    """
    Split text on every top-level 'def name(' or 'async def name('.
    Pattern is local — no global variables.
    """
    toplevel_def_pat = re.compile(
        r'^(?:async\s+def|def)\s+([A-Za-z_]\w*)\s*\(',
        re.MULTILINE,
    )

    matches = list(toplevel_def_pat.finditer(text))
    if not matches:
        return {}, ["No top-level 'def name(' blocks found."]

    header = text[: matches[0].start()] if include_header_imports else ""
    out: Dict[str, str] = {}

    for i, m in enumerate(matches):
        name = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].rstrip() + "\n"
        out[f"{name}.py"] = (header + body) if include_header_imports else body

    return out, []
