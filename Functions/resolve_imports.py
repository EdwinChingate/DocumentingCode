from __future__ import annotations

from default_stdlib_names import *
from default_third_party_map import *



def resolve_imports(
    external_names   : Set[str],
    func_to_module   : Dict[str, str],
    third_party_map  : Dict[str, str] | None = None,
    extra_stdlib     : Set[str]        | None = None,
) -> Tuple[List[str], List[str]]:
    """
    Classify every name in external_names into one of:
        1. third-party alias  →  "import pandas as pd"
        2. stdlib             →  "import re"
        3. known module       →  "from ModuleName import *"
        4. truly unknown      →  returned as a separate list

    func_to_module should be the already-merged map:
        bundle-internal functions + custom folder functions.

    Returns (import_lines, unknown_names).
    No global variables, no classes.
    """
    tp_map = {**default_third_party_map(), **(third_party_map or {})}
    stdlib = default_stdlib_names() | (extra_stdlib or set())

    import_lines : List[str] = []
    unknown      : List[str] = []
    seen         : Set[str]  = set()

    for name in sorted(external_names):
        if name in tp_map:
            line = tp_map[name]
            if line not in seen:
                import_lines.append(line)
                seen.add(line)

        elif name in stdlib:
            line = f"import {name}"
            if line not in seen:
                import_lines.append(line)
                seen.add(line)

        elif name in func_to_module:
            line = f"from {func_to_module[name]} import *"
            if line not in seen:
                import_lines.append(line)
                seen.add(line)

        else:
            unknown.append(name)

    return import_lines, unknown
