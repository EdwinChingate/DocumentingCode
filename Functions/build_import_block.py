from __future__ import annotations

# TODO: could not auto-resolve the following names —
#   from ??? import n



def build_import_block(
    import_lines : List[str],
    unknown      : List[str],
) -> str:
    """
    Assemble the final import block string.
    Unknown names become visible TODO comments — nothing is silently lost.
    No global variables, no classes.
    """
    parts: List[str] = []

    if import_lines:
        parts.append("\n".join(import_lines))

    if unknown:
        todo = (
            "# TODO: could not auto-resolve the following names —\n"
            + "\n".join(f"#   from ??? import {n}" for n in sorted(unknown))
        )
        parts.append(todo)

    return "\n".join(parts) + "\n" if parts else ""
