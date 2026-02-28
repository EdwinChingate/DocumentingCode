import os
import json
import numpy as np
import pandas as pd


def save_project_snapshot(
    output_folder,
    FunctionsListDF,
    CallsMat,
    InputsMat=None,
    OutputsMat=None
):
    """
    Save adjacency matrices and structural metadata
    for documentation planning.
    """

    os.makedirs(output_folder, exist_ok=True)

    # --- Function names ---
    function_names = FunctionsListDF["Documentation"].values

    # --- Calls adjacency (numpy raw) ---
    np.save(os.path.join(output_folder, "calls_matrix.npy"), CallsMat)

    # --- Calls adjacency (labeled CSV) ---
    CallsDF = pd.DataFrame(
        CallsMat,
        index=function_names,
        columns=function_names
    )
    CallsDF.to_csv(os.path.join(output_folder, "calls_matrix.csv"))

    # --- Inputs matrix ---
    if InputsMat is not None:
        InputsDF = pd.DataFrame(InputsMat)
        InputsDF.to_csv(os.path.join(output_folder, "inputs_matrix.csv"))

    # --- Outputs matrix ---
    if OutputsMat is not None:
        OutputsDF = pd.DataFrame(OutputsMat)
        OutputsDF.to_csv(os.path.join(output_folder, "outputs_matrix.csv"))

    # --- Structural metrics for planning ---
    in_degree = CallsMat.sum(axis=0)
    out_degree = CallsMat.sum(axis=1)

    metrics_df = pd.DataFrame({
        "function": function_names,
        "in_degree": in_degree,
        "out_degree": out_degree
    })

    metrics_df.sort_values("out_degree", ascending=False)\
              .to_csv(os.path.join(output_folder, "function_metrics.csv"),
                      index=False)

    # --- JSON summary ---
    summary = {
        "n_functions": int(len(function_names)),
        "n_edges": int(CallsMat.sum()),
        "max_in_degree": int(in_degree.max()),
        "max_out_degree": int(out_degree.max())
    }

    with open(os.path.join(output_folder, "summary.json"), "w") as f:
        json.dump(summary, f, indent=4)

    print(f"Project snapshot saved in: {output_folder}")


from __future__ import annotations

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd


def _dt_utc(ts: float) -> str:
    """Unix timestamp -> ISO8601 UTC string."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def get_file_times(path: Path) -> dict:
    """
    Returns filesystem timestamps for a file.
    On Linux, 'ctime' is NOT creation time; it's metadata-change time.
    On some systems, st_birthtime may exist (true creation time).
    """
    st = path.stat()

    out = {
        "path": str(path),
        "mtime_utc": _dt_utc(st.st_mtime),
        "ctime_utc": _dt_utc(st.st_ctime),
        "size_bytes": int(st.st_size),
    }

    # True birth time exists on some platforms / filesystems
    birth = getattr(st, "st_birthtime", None)
    out["birthtime_utc"] = _dt_utc(birth) if birth is not None else None

    return out


def get_git_times(repo_root: Path, file_path: Path) -> dict | None:
    """
    Get first/last commit timestamps for a file using git.
    Returns None if git fails (e.g., not a git repo).
    """
    try:
        rel = file_path.resolve().relative_to(repo_root.resolve())
    except Exception:
        rel = file_path

    def _run(args: list[str]) -> str:
        return subprocess.check_output(
            args,
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()

    try:
        # Last commit time (unix epoch)
        last_ts = _run(["git", "log", "-1", "--format=%ct", "--", str(rel)])
        # First commit time (unix epoch) -> use reverse log
        first_ts = _run(["git", "log", "--reverse", "-1", "--format=%ct", "--", str(rel)])

        return {
            "git_last_commit_utc": _dt_utc(float(last_ts)) if last_ts else None,
            "git_first_commit_utc": _dt_utc(float(first_ts)) if first_ts else None,
        }
    except Exception:
        return None


from pathlib import Path
import pandas as pd

def add_time_metadata_to_functions_list(
    FunctionsFolder: str | Path,
    FunctionsListDF: pd.DataFrame,
    repo_root: str | Path | None = None,
    include_git: bool = True,
    dedupe_left: bool = True,
    show_duplicates: int = 20,
) -> pd.DataFrame:
    FunctionsFolder = Path(FunctionsFolder)
    repo_root = Path(repo_root) if repo_root is not None else None

    if "Documentation" not in FunctionsListDF.columns:
        raise KeyError("FunctionsListDF must contain a 'Documentation' column.")

    out_df = FunctionsListDF.copy()
    out_df["Documentation"] = out_df["Documentation"].astype("string").str.strip()

    # Drop missing/empty docs
    missing_mask = out_df["Documentation"].isna() | (out_df["Documentation"] == "")
    if missing_mask.any():
        print("Warning: missing/empty Documentation rows (showing first 10):")
        print(out_df.loc[missing_mask].head(10))
        out_df = out_df.loc[~missing_mask].copy()

    # Duplicate check
    dup_mask = out_df["Documentation"].duplicated(keep=False)
    if dup_mask.any():
        vc = out_df.loc[dup_mask, "Documentation"].value_counts()
        print(f"Warning: {vc.size} duplicated Documentation values.")
        print("Top duplicates:")
        print(vc.head(show_duplicates))

        if dedupe_left:
            out_df = out_df.drop_duplicates(subset=["Documentation"], keep="first").copy()
            print(f"Deduped left DF: now {len(out_df)} unique functions.")

    rows = []
    for fn in out_df["Documentation"].astype(str).values:
        file_path = FunctionsFolder / f"{fn}.py"

        if not file_path.exists():
            rows.append({
                "Documentation": fn,
                "file_exists": False,
                "path": str(file_path),
                "mtime_utc": None,
                "ctime_utc": None,
                "birthtime_utc": None,
                "size_bytes": None,
                "git_first_commit_utc": None,
                "git_last_commit_utc": None,
            })
            continue

        t = get_file_times(file_path)
        row = {
            "Documentation": fn,
            "file_exists": True,
            **t,
            "git_first_commit_utc": None,
            "git_last_commit_utc": None,
        }

        if include_git and repo_root is not None:
            gt = get_git_times(repo_root, file_path)
            if gt:
                row.update(gt)

        rows.append(row)

    TimesDF = pd.DataFrame(rows)
    TimesDF["Documentation"] = TimesDF["Documentation"].astype("string").str.strip()

    # Right side should be unique; if not, something is off in file mapping
    if TimesDF["Documentation"].duplicated().any():
        print("Warning: TimesDF has duplicate Documentation keys (unexpected).")
        print(TimesDF["Documentation"].value_counts().head(20))

    merged = out_df.merge(TimesDF, on="Documentation", how="left", validate="many_to_one")
    return merged


from pathlib import Path
from datetime import datetime, timezone


def add_last_modification_time(FunctionsFolder, FunctionsListDF):
    FunctionsFolder = Path(FunctionsFolder)
    df = FunctionsListDF.copy()

    df["Documentation"] = df["Documentation"].astype(str).str.strip()

    mtime_list = []

    for fn in FunctionsListDF.index:
        file_path = FunctionsFolder / f"{fn}.py"

        if file_path.exists():
            ts = file_path.stat().st_mtime
            mtime_list.append(
                datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
            )
        else:
            mtime_list.append(None)

    df["last_modified_utc"] = mtime_list

    return df


def save_functions_metadata(output_folder: str | Path, FunctionsListDF: pd.DataFrame) -> None:
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    FunctionsListDF.to_csv(output_folder / "functions_metadata.csv", index=False)

    # Also save a minimal JSON summary for quick reads
    meta = {
        "n_functions": int(len(FunctionsListDF)),
        "n_missing_files": int((~FunctionsListDF["file_exists"]).sum()) if "file_exists" in FunctionsListDF else None,
        "latest_mtime_utc": (
            FunctionsListDF["mtime_utc"].dropna().max()
            if "mtime_utc" in FunctionsListDF else None
        ),
        "latest_git_commit_utc": (
            FunctionsListDF["git_last_commit_utc"].dropna().max()
            if "git_last_commit_utc" in FunctionsListDF else None
        ),
    }
    with open(output_folder / "functions_metadata_summary.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)



