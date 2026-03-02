from __future__ import annotations
from pathlib import Path
from get_external_names import *
from get_top_level_defs import *
from parse_bundle import *
from scan_custom_folder import *
from strip_existing_imports import *

def SplitAndRepairBundle(
    bundle_path: str | Path,
    output_dir: str | Path,
    custom_functions_dir: str | Path | None = None,
    overwrite: bool = True
) -> Dict[str, Any]:
    """Orchestrates parsing, import resolution, and file generation."""
    bundle_path = Path(bundle_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = bundle_path.read_text(encoding="utf-8", errors="replace")
    files_dict = parse_bundle(text)

    # Dictionary to hold definition names to module names
    master_def_map: Dict[str, str] = {}
    
    # 1. Map definitions from inside the bundle
    for fname, code in files_dict.items():
        module_name = Path(fname).stem
        for def_name in get_top_level_defs(code):
            master_def_map[def_name] = module_name
            
    # 2. Map definitions from external library folder
    if custom_functions_dir:
        custom_map = scan_custom_folder(Path(custom_functions_dir))
        master_def_map.update(custom_map)

    # 3. Process individual files
    third_party = {"np": "import numpy as np", "pd": "import pandas as pd"}
    stdlib = {"re", "os", "sys", "json", "math", "time", "pathlib", "typing", "ast"}

    results: Dict[str, Any] = {"written": [], "skipped": []}

    for fname, code in files_dict.items():
        out_path = output_dir / fname
        if out_path.exists() and not overwrite:
            results["skipped"].append(str(out_path))
            continue

        externals = get_external_names(code)
        
        import_lines = []
        unknowns = []
        seen = set()

        for name in sorted(externals):
            line = None
            if name in third_party:
                line = third_party[name]
            elif name in stdlib:
                line = f"import {name}"
            elif name in master_def_map:
                line = f"from {master_def_map[name]} import *"
            else:
                unknowns.append(name)

            if line and line not in seen:
                import_lines.append(line)
                seen.add(line)

        # Build file text
        new_header = "\n".join(import_lines) + ("\n\n" if import_lines else "")
        if unknowns:
            new_header += f"# TODO: unresolved names: {', '.join(unknowns)}\n\n"
            
        clean_body = strip_existing_imports(code)
        final_code = f"from __future__ import annotations\n{new_header}{clean_body}"

        out_path.write_text(final_code, encoding="utf-8")
        results["written"].append(str(out_path))
        print(f"✅ Wrote {out_path.name} ({len(import_lines)} imports fixed)")

    return results
