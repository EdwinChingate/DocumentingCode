from __future__ import annotations



def assemble_file(import_block: str, cleaned_body: str) -> str:
    """
    Combine __future__, import block, and cleaned body into one string.
    No global variables, no classes.
    """
    future_line = "from __future__ import annotations\n"

    parts: List[str] = [future_line]

    if import_block.strip():
        parts.append(import_block)

    parts.append("\n")
    parts.append(cleaned_body)

    result = "\n".join(parts)
    return result if result.endswith("\n") else result + "\n"
