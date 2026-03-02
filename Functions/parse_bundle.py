from __future__ import annotations
import re
def parse_bundle(text: str) -> Dict[str, str]:
    """Parses a bundle file into a dictionary of filenames to code."""
    pattern = re.compile(r"^\s*#\s*---\s*(?P<name>[^-].*?)\s*---\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    files: Dict[str, str] = {}
    
    for i, m in enumerate(matches):
        name = m.group("name").strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        files[name] = text[start:end].strip("\n")
        
    return files
