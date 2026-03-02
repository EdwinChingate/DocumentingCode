from __future__ import annotations
def strip_existing_imports(code: str) -> str:
    """Removes the top import block and docstrings from a file's code."""
    lines = code.splitlines()
    i = 0
    in_doc = False
    delim = None
    
    while i < len(lines):
        s = lines[i].strip()
        if in_doc:
            if delim and delim in lines[i]: 
                in_doc = False
            i += 1
            continue
        if s == "" or s.startswith("#"):
            i += 1
            continue
        if s.startswith(('"""', "'''")):
            in_doc = True
            delim = s[:3]
            i += 1
            if s.count(delim) >= 2: 
                in_doc = False
            continue
        if s.startswith("from __future__ import ") or s.startswith("import ") or s.startswith("from "):
            i += 1
            continue
        break
        
    return "\n".join(lines[i:]).lstrip("\n")