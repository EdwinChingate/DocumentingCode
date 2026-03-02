from __future__ import annotations

from get_module_path_from_file import *
from is_system_path import *
from top_level_function_defs import *



def collect_functions_from_paths(
    paths: List[str | Path],
    verbose: bool = True,
) -> Dict[str, str]:
    """
    Scan a list of flat folders for .py files and collect all top-level
    function and class definitions, mapping each name to its module stem.

    Rules:
        - Only scans files directly inside each folder (no subdirectories).
        - Skips dunder files (__init__.py, __main__.py, etc.).
        - Refuses to scan system/site-packages paths.
        - Each file is assumed to be named after its main function.

    Returns:
        { function_name : module_stem }
        e.g. { "AlignedFragmentsMat": "AlignedFragmentsMat", ... }

    No global variables, no classes.
    """
    func_to_module: Dict[str, str] = {}

    for root_path_str in paths:
        root_path = Path(root_path_str).resolve()

        if is_system_path(root_path):
            raise ValueError(
                f"[collect_functions_from_paths] Refusing to scan "
                f"system folder:\n  {root_path}\n"
                f"Please pass the path to YOUR personal functions folder."
            )

        if not root_path.exists():
            if verbose:
                print(f"[collect_functions_from_paths] "
                      f"Path not found, skipping: {root_path}")
            continue

        if not root_path.is_dir():
            if verbose:
                print(f"[collect_functions_from_paths] "
                      f"Not a directory, skipping: {root_path}")
            continue

        for py_file in sorted(root_path.iterdir()):

            if not py_file.is_file():
                continue

            if py_file.suffix != ".py":
                continue

            if py_file.stem.startswith("__") and py_file.stem.endswith("__"):
                continue

            stem = py_file.stem

            try:
                source    = py_file.read_text(encoding="utf-8", errors="replace")
                defs      = top_level_function_defs(source)
                mod_path  = get_module_path_from_file(py_file, root_path)

                if defs:
                    for def_name in defs:
                        func_to_module[def_name] = mod_path
                else:
                    # fallback: map the stem to itself
                    func_to_module[stem] = stem

            except Exception as exc:
                if verbose:
                    print(f"[collect_functions_from_paths] "
                          f"Could not process '{py_file}': {exc}")

    return func_to_module
