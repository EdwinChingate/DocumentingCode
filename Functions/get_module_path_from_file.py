from __future__ import annotations



def get_module_path_from_file(py_file: Path, root_path: Path) -> str:
    """
    Convert a .py file path to a dotted Python import path,
    relative to root_path.

    Example:
        root_path = /project/MyFunctions
        py_file   = /project/MyFunctions/sub/MyFunc.py
        returns   → "sub.MyFunc"

    Uses os.sep instead of Path.sep (Path.sep does not exist).
    No global variables, no classes.
    """
    relative  = py_file.relative_to(root_path)
    no_suffix = str(relative.with_suffix(""))
    return no_suffix.replace(os.sep, ".")
