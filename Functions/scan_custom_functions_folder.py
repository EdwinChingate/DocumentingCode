from __future__ import annotations



def scan_custom_functions_folder(folder: str | Path) -> Dict[str, str]:
    """
    Scan a folder of .py files where every file is named after
    the function it contains (e.g. MyFunc.py contains def MyFunc(...)).

    Returns a dict mapping function_name -> module_stem, e.g.:
        {
            "AlignedFragmentsMat"      : "AlignedFragmentsMat",
            "ConsensusSpectra"         : "ConsensusSpectra",
            "Feature_Module"           : "Feature_Module",
            ...
        }

    No global variables, no classes.
    """
    folder = Path(folder)
    if not folder.exists():
        raise FileNotFoundError(f"Custom functions folder not found: {folder}")

    func_to_module: Dict[str, str] = {}

    for py_file in sorted(folder.glob("*.py")):
        stem   = py_file.stem
        source = py_file.read_text(encoding="utf-8", errors="replace")

        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue

        found_any = False
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_to_module[node.name] = stem
                found_any = True

        # If no function was found by AST, fall back to the filename itself.
        # This covers edge cases where the file defines a function with
        # a slightly different name but we still want the stem resolvable.
        if not found_any:
            func_to_module[stem] = stem

    return func_to_module
