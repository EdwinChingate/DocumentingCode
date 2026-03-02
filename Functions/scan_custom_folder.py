from __future__ import annotations
from get_top_level_defs import *

def scan_custom_folder(folder_path: Path) -> Dict[str, str]:
    """Maps custom function names found in a directory to their import paths."""
    mapping: Dict[str, str] = {}
    if not folder_path.is_dir(): 
        return mapping
    
    for py_file in folder_path.rglob("*.py"):
        try:
            code = py_file.read_text(encoding="utf-8", errors="replace")
            # Note: relies on get_top_level_defs being imported/available
            defs = get_top_level_defs(code)
            
            # This fixes the os.sep bug natively by using pure POSIX strings
            mod_path = py_file.relative_to(folder_path).with_suffix("").as_posix().replace("/", ".")
            for d in defs:
                mapping[d] = mod_path
        except Exception:
            continue
            
    return mapping