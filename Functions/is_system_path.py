from __future__ import annotations

# TODO: could not auto-resolve the following names —
#   from ??? import marker



def is_system_path(folder: Path) -> bool:
    """
    Return True if folder looks like a system or site-packages location
    that should never be scanned.
    No global variables, no classes.
    """
    system_markers = (
        "site-packages",
        "dist-packages",
        "/usr/lib",
        "/usr/local/lib",
        "/snap/",
        "\\Python\\Lib",
        "\\site-packages",
    )
    folder_str = str(folder)
    return any(marker in folder_str for marker in system_markers)
