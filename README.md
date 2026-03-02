![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

![[]](https://github.com/EdwinChingate/MobiObs/blob/main/MobiObs.png)

# MobiObs

**MobiObs** is a lightweight, opinionated toolkit for structurally documenting and transforming Python codebases built around the pattern **“one function per file.”**

It extracts dependency structure, generates documentation artifacts, visualizes function relationships in Obsidian Canvas, and now supports reversible code bundling and reconstruction.

The goal is clarity and structural control over modular utility repositories.

---

## Core Capabilities

MobiObs provides:

### 1. Static Function Analysis

* Extracts a **function call graph** (who calls whom).
* Parses **inputs** (from `def ...(...)`) and **outputs** (from `return ...`).
* Detects internal dependencies via AST inspection.

### 2. Per-Function Markdown Documentation

* Generates **one Markdown file per function**.
* Creates Obsidian-friendly **wiki links** between related functions.
* Supports prefix-based naming for integration inside vaults.

### 3. Obsidian Canvas Visualization

* Produces a `.canvas` JSON file where each node represents a function doc.
* Arranges nodes as a dependency tree.
* Supports geometry-aware ordering for structural depth representation.

---

## New Structural Features

Recent additions extend the project beyond documentation into structural code transformation.

### 4. Canvas → Code Bundle (Reversible Flattening)

`CanvasToCombinedTxt(...)` can:

* Read a selected function subgraph from an Obsidian Canvas.
* Export only those functions into a single `.txt` bundle.
* Order functions **from deepest dependency to root**.
* Use consistent `# --- Function.py ---` separators.
* Insert configurable blank spacing for editing.
* Automatically comment internal `from X import *` imports if `X` is also part of the bundle.

This produces a self-contained, editable code bundle without breaking dependency structure.

---

### 5. Bundle → Split + Dependency Repair

`SplitAndRepairBundle(...)` can:

* Parse a bundled `.txt` file.
* Split it back into individual `.py` files.
* Detect which functions call which other bundled functions.
* Automatically restore required imports.
* Uncomment previously neutralized internal imports.
* Safely skip malformed or empty fragments.

This makes the flattening process fully reversible.

---

### 6. Dependency-Aware Ordering

Function export order can now be based on:

* Canvas geometry (deepest nodes first).
* Explicit file markers.
* Top-level definition parsing.

This allows:

* Logical build-order exports.
* Cleaner editing workflows.
* Structural introspection.

---

## Installation

This repository currently behaves as a structured script toolbox rather than a packaged library.

### Requirements

* Python 3.9+
* `numpy`
* `pandas`
* Optional: `tabulate`, `IPython` (for notebook display)

### Setup

Clone the repository and ensure the `Functions/` directory is on your `PYTHONPATH`, or execute from a notebook/script that can import the modules directly.

---

## Quickstart – Documentation Pipeline

The main orchestrator:

```python
from FolderToCanvas import FolderToCanvas

canvas = FolderToCanvas(
    FunctionsFolder="/path/to/Functions",
    SaveFolder="/path/to/generated_docs",
    OutputCanvasPath="/path/to/FunctionsMap.canvas",
    VaultDocPath="01-Projects/MyProject/docs",
    prefix="myproj_"
)
```

This generates:

* Markdown documentation per function.
* An Obsidian Canvas file visualizing dependencies.

---

## Quickstart – Bundle / Reconstruction Workflow

### Export a subgraph from Canvas

```python
from CanvasToCombinedTxt import CanvasToCombinedTxt

CanvasToCombinedTxt(
    canvas_path="MyMap.canvas",
    functions_folder="Functions",
    output_txt_path="SelectedBundle.txt",
    gap_lines=4
)
```

### Split and repair the bundle

```python
from SplitAndRepairBundle import SplitAndRepairBundle

summary = SplitAndRepairBundle(
    bundle_txt_path="SelectedBundle.txt",
    output_folder="Functions_RESTORED",
    overwrite=True,
    repair_headers=True
)
```

This restores fully functional modules with correct imports.

---

## Design Assumptions

MobiObs works best when:

* Each file contains **one top-level function**.
* Internal dependencies use `from X import *` or explicit imports.
* The codebase is structured as composable utilities rather than monolithic classes.

The toolkit intentionally favors explicit structural simplicity over framework complexity.

---

## Where This Project Is Heading

MobiObs is evolving toward:

* A lightweight **Obsidian-integrated structural code notebook**.
* Bidirectional transformation between:

  * Code → Graph → Editable Bundle → Code
* Dependency-aware execution planning.
* Possible plugin layer to orchestrate Python execution from inside Obsidian.

The focus remains practical: improving cognitive control over modular Python repositories without introducing heavy build systems or large frameworks.

---

## Philosophy

This project is not a documentation generator alone.

It is a structural introspection and transformation toolkit designed for developers who:

* Work with many small utility modules.
* Prefer explicit dependency graphs.
* Want reversible transformations between structure and text.
* Use Obsidian as a thinking environment.
