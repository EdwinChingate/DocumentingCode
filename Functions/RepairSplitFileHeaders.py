from __future__ import annotations

from assemble_file import *
from build_import_block import *
from collect_functions_from_paths import *
from get_external_names import *
from resolve_imports import *
from strip_existing_imports import *
from top_level_function_defs import *
# TODO: could not auto-resolve the following names —
#   from ??? import fname
#   from ??? import import_lines
#   from ??? import unknown



def RepairSplitFileHeaders(
    files_dict           : Dict[str, str],
    custom_modules_paths : List[str | Path] | None = None,
    import_style         : str                     = "star",
    third_party_map      : Dict[str, str]  | None  = None,
    extra_stdlib         : Set[str]        | None  = None,
    verbose              : bool                    = True,
) -> Tuple[Dict[str, str], Dict]:
    """
    For every file in files_dict:
      1. Build func→module map from all bundle files.
      2. Extend that map by scanning custom_modules_paths (if provided).
      3. Collect all names used in each file.
      4. Subtract locally defined names.
      5. Resolve what remains to exact import lines.
      6. Strip old imports, prepend new ones.

    Returns (repaired_files_dict, debug_info).
    No global variables, no module-level classes.
    """
    # ── Pass 1: bundle-internal func → module map ─────────────────────────
    bundle_func_to_module : Dict[str, str]      = {}
    file_to_defs          : Dict[str, Set[str]] = {}

    for fname, code in files_dict.items():
        stem = Path(fname).stem
        defs = top_level_function_defs(code or "")
        file_to_defs[fname] = defs
        for d in defs:
            bundle_func_to_module[d] = stem

    # ── Pass 2: custom folder func → module map ───────────────────────────
    custom_func_to_module: Dict[str, str] = {}
    if custom_modules_paths:
        if verbose:
            print(
                f"[RepairSplitFileHeaders] Scanning custom paths: "
                f"{custom_modules_paths}"
            )
        custom_func_to_module = collect_functions_from_paths(
            custom_modules_paths,
            verbose=verbose,
        )
        if verbose:
            print(
                f"[RepairSplitFileHeaders] Found {len(custom_func_to_module)} "
                f"functions in custom paths."
            )

    # bundle-internal definitions take priority over custom folder
    merged_func_to_module: Dict[str, str] = {
        **custom_func_to_module,
        **bundle_func_to_module,
    }

    # ── Pass 3: repair each file ──────────────────────────────────────────
    new_files : Dict[str, str] = {}
    debug     : Dict           = {"imports_added": {}, "unknown_names": {}}

    for fname, code in files_dict.items():
        code      = code or ""
        defs_here = file_to_defs.get(fname, set())

        external = get_external_names(code) - defs_here

        import_lines, unknown = resolve_imports(
            external_names  = external,
            func_to_module  = merged_func_to_module,
            third_party_map = third_party_map,
            extra_stdlib    = extra_stdlib,
        )

        if verbose and unknown:
            print(
                f"[RepairSplitFileHeaders] {fname}: "
                f"still unresolved → {sorted(unknown)}"
            )

        import_block = build_import_block(import_lines, unknown)
        body         = strip_existing_imports(code)
        fixed        = assemble_file(import_block, body)

        new_files[fname]              = fixed
        debug["imports_added"][fname] = import_lines
        debug["unknown_names"][fname] = unknown

    return new_files, debug
