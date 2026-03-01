from _parse_by_file_markers import *
from _parse_by_toplevel_defs import *

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


_FILE_MARKER_PATTERNS = [
    re.compile(r'^\s*#\s*---\s*(.+?\.py)\s*---\s*$'),    # "# --- Name.py ---"
    re.compile(r'^\s*---\s*(.+?\.py)\s*---\s*$'),        # "--- /path/Name.py ---"
]

_SEPARATOR_PAT = re.compile(r'^\s*#\s*#{20,}\s*$')        # lines like "###########..."


def SplitBundleTxtToPyFiles(
    bundle_txt_path: str | Path,
    output_folder: str | Path,
    overwrite: bool = False,
    include_header_imports_in_def_mode: bool = True,
    encoding: str = "utf-8",
) -> Dict:
    """
    Read a bundle .txt and write individual .py files.

    Parsing modes:
      1) If file markers are present ("# --- Name.py ---" or "--- /path/Name.py ---"),
         split by markers (reliable).
      2) Else fallback to splitting by top-level `def name(` (heuristic).

    Returns a summary dict.
    """
    bundle_txt_path = Path(bundle_txt_path)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    if not bundle_txt_path.exists():
        raise FileNotFoundError(f"Bundle file not found: {bundle_txt_path}")

    text = bundle_txt_path.read_text(encoding=encoding, errors="replace")

    # Try markers first
    files_dict, notes = _parse_by_file_markers(text)

    mode = "file_markers"
    if not files_dict:
        # Fallback: def-mode
        files_dict, notes2 = _parse_by_toplevel_defs(text, include_header_imports=include_header_imports_in_def_mode)
        notes.extend(notes2)
        mode = "toplevel_defs"

    written = []
    skipped = []
    for fname, content in files_dict.items():
        out_path = output_folder / fname
        if out_path.exists() and not overwrite:
            skipped.append(str(out_path))
            continue
        out_path.write_text(content, encoding=encoding)
        written.append(str(out_path))

    return {
        "mode": mode,
        "bundle_txt_path": str(bundle_txt_path),
        "output_folder": str(output_folder),
        "n_detected": len(files_dict),
        "n_written": len(written),
        "n_skipped": len(skipped),
        "written": written,
        "skipped": skipped,
        "notes": notes,
    }
