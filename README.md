![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# DocumentingCode

**DocumentingCode** is a small, opinionated toolkit to **auto-document a folder of Python utility functions** by:

- extracting a **function call graph** (who calls whom),
- extracting **inputs** (from `def ...(...)`) and **outputs** (from `return ...`),
- generating **one Markdown doc per function** (Obsidian-friendly),
- generating an **Obsidian Canvas** JSON that visualizes your codebase as a dependency tree of linked docs.

It’s made for the “I have 80 tiny `.py` files and my brain is now a swap file” situation.

---

## What it generates

Given a folder where each file is roughly “one function per file”, DocumentingCode can generate:

1. **Markdown docs** per function (with wiki links between related functions and variables)
2. A **Canvas map** (`.canvas` JSON) where each node is a doc file, arranged as a dependency tree

---

## Installation

This repo currently behaves like a **script toolbox**, not a packaged library.

### Requirements
- Python 3.9+ recommended
- `numpy`
- `pandas`
- Optional (only for pretty notebook display): `tabulate`, `IPython`

### Setup
Clone the repo and make sure the `Functions/` directory is on your `PYTHONPATH`, or run from a notebook/script that can import those modules.

---

## Quickstart (the main pipeline)

The “one-call” orchestrator is `FolderToCanvas(...)`.

```python
from FolderToCanvas import FolderToCanvas

FunctionsFolder   = "/path/to/your/repo/Functions"
SaveFolder        = "/path/to/save/generated_docs"
OutputCanvasPath  = "/path/to/save/FunctionsMap.canvas"   # JSON file Obsidian can open
VaultDocPath      = "01-Projects/MyProject/docs"          # path *inside* your vault

canvas = FolderToCanvas(
    FunctionsFolder=FunctionsFolder,
    SaveFolder=SaveFolder,
    OutputCanvasPath=OutputCanvasPath,
    VaultDocPath=VaultDocPath,
    prefix="myproj_"   # prefix for doc filenames and Obsidian links
)
