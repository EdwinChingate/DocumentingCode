from __future__ import annotations
from pathlib import Path
from typing import Dict

from parse_bundle import parse_bundle
from RepairSplitFileHeaders import RepairSplitFileHeaders


def SplitAndRepairBundle(
    bundle_txt_path: str | Path,
    output_folder:   str | Path,
    overwrite:       bool = False,
    keep_empty:      bool = False,
    repair_headers:  bool = True,
    import_style:    str  = "star",
    verbose:         bool = True,
) -> Dict:
    """
    Full pipeline:
      read bundle → parse into files → repair imports → write to disk.
    No global variables.
    """
    bundle_txt_path = Path(bundle_txt_path)
    output_folder   = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    text = bundle_txt_path.read_text(encoding="utf-8", errors="replace")
    files_dict, notes, mode = parse_bundle(text)

    # Identify problematic entries
    bad   = {k for k, v in files_dict.items() if v is None}
    empty = {k for k, v in files_dict.items()
             if isinstance(v, str) and not v.strip()}

    if verbose and (bad or empty):
        print(f"[SplitAndRepairBundle] mode={mode}  None={len(bad)}  empty={len(empty)}")
        if bad:   print("  None  keys:", list(bad)[:20])
        if empty: print("  Empty keys:", list(empty)[:20])

    if not keep_empty:
        for k in bad | empty:
            files_dict.pop(k, None)

    debug = {"imports_added": {}}
    if repair_headers and files_dict:
        files_dict, debug = RepairSplitFileHeaders(files_dict, import_style=import_style)

    written     : list = []
    skipped     : list = []
    type_errors : list = []

    for fname, content in files_dict.items():
        out_path = output_folder / fname

        if out_path.exists() and not overwrite:
            skipped.append(str(out_path))
            continue

        if not isinstance(content, str):
            type_errors.append((fname, type(content).__name__))
            if verbose:
                print(f"[SplitAndRepairBundle] SKIP non-str: {fname} → {type(content).__name__}")
            continue

        out_path.write_text(content, encoding="utf-8")
        written.append(str(out_path))
        if verbose:
            print(f"  wrote → {out_path}")

    return {
        "mode"                      : mode,
        "written"                   : written,
        "skipped"                   : skipped,
        "n_written"                 : len(written),
        "n_detected_after_cleaning" : len(files_dict),
        "type_errors"               : type_errors,
        "notes"                     : notes,
        "imports_added"             : debug.get("imports_added", {}),
    }
