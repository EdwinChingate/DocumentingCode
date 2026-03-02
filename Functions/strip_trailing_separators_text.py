import re

def strip_trailing_separators_text(s: str) -> str:
    """
    Remove trailing separator blocks like long hash lines + surrounding blanks.
    Self-contained: does not rely on any global constants imported from other files.
    """
    separator_hashline = re.compile(r'^\s*#\s*#{20,}\s*$')

    lines = s.splitlines()
    i = len(lines)
    while i > 0:
        line = lines[i - 1].strip()
        if line == "" or separator_hashline.match(lines[i - 1]) is not None:
            i -= 1
        else:
            break

    out = "\n".join(lines[:i]).rstrip()
    return out + ("\n" if out else "")
