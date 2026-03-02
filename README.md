![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

![[]](https://github.com/EdwinChingate/MobiObs/blob/main/MobiObs.png)

# MobiObs

**MobiObs** began as a pragmatic solution to a common developer problem: too many small Python utility files and too little cognitive clarity.

It has evolved into a lightweight structural analysis and transformation framework for modular Python codebases built around the pattern **“one function per file.”**

MobiObs does not just generate documentation.
It makes repository architecture visible, editable, and reversible.

The core workflow:

```
Code (.py)
   ↓
Structured Docs (.md)
   ↓
Dependency Graph (.canvas)
   ↓
Editable Bundle
   ↓
Reconstructed Modules
```

This cycle allows you to move between code and structure without losing dependency integrity.

---

## Core Capabilities

### 1. Static Function Analysis

* Extracts a **function call graph** (who calls whom).
* Parses **inputs** (from `def ...(...)`) and **outputs** (from `return ...`).
* Detects internal dependencies using AST inspection.

### 2. Per-Function Markdown Documentation

* Generates **one Markdown file per function**.
* Creates Obsidian-compatible wiki links.
* Supports prefix-based naming for vault integration.

### 3. Obsidian Canvas Visualization

* Produces a `.canvas` JSON file.
* Each node represents a function document.
* Nodes are arranged as a dependency tree.
* Supports geometry-aware structural depth ordering.

This makes the codebase navigable as architecture, not just text.

---

## Structural Transformation Features

MobiObs now supports reversible structural workflows.

### 4. Canvas → Code Bundle (Reversible Flattening)

`CanvasToCombinedTxt(...)`:

* Exports a selected function subgraph.
* Orders functions deepest dependency → root.
* Uses clear `# --- Function.py ---` separators.
* Inserts configurable spacing for editing.
* Automatically neutralizes internal imports when bundled.

This produces a structurally consistent, editable code bundle.

---

### 5. Bundle → Split + Dependency Repair

`SplitAndRepairBundle(...)`:

* Parses bundled text.
* Splits into individual `.py` files.
* Detects call relationships between bundled functions.
* Restores required imports automatically.
* Safely handles malformed or empty fragments.

The flattening process is fully reversible.

---

### 6. Dependency-Aware Ordering

Export order can be derived from:

* Canvas geometry.
* Explicit markers.
* Top-level definition parsing.

This supports logical build-order reconstruction and cleaner editing workflows.

---

## Installation

This repository behaves as a structured script toolbox rather than a packaged library.

### Requirements

* Python 3.9+
* `numpy`
* `pandas`
* Optional: `tabulate`, `IPython`

### Setup

Clone the repository and ensure the `Functions/` directory is on your `PYTHONPATH`, or execute from a script/notebook that can import the modules directly.

---

## Quickstart – Documentation Pipeline

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

Generates:

* Markdown documentation per function.
* An Obsidian Canvas file visualizing dependencies.

---

## Quickstart – Bundle / Reconstruction Workflow

### Export a subgraph

```python
from CanvasToCombinedTxt import CanvasToCombinedTxt

CanvasToCombinedTxt(
    canvas_path="MyMap.canvas",
    functions_folder="Functions",
    output_txt_path="SelectedBundle.txt",
    gap_lines=4
)
```

### Split and repair

```python
from SplitAndRepairBundle import SplitAndRepairBundle

summary = SplitAndRepairBundle(
    bundle_txt_path="SelectedBundle.txt",
    output_folder="Functions_RESTORED",
    overwrite=True,
    repair_headers=True
)
```

Restores fully functional modules with correct imports.

---

## Design Assumptions

MobiObs works best when:

* Each file contains **one top-level function**.
* Dependencies use explicit imports or `from X import *`.
* The repository is composed of small utilities rather than large frameworks.

The system favors structural clarity over abstraction density.

---

## Direction

MobiObs is evolving toward:

* A lightweight **Obsidian-integrated structural code notebook**.

* Bidirectional transformation between:

  ```
  Code → Graph → Editable Bundle → Code
  ```

* Dependency-aware execution planning.

* A possible Obsidian plugin layer for orchestrating Python workflows inside the vault.

The aim is practical: improve cognitive control over modular repositories without introducing heavy build systems.

---

## Philosophy

This is not just a documentation generator.

MobiObs is a structural introspection layer for developers who:

* Work with many small modules.
* Prefer explicit dependency graphs.
* Want reversible structural transformations.
* Use Obsidian as a thinking environment.

It helps you reason about your codebase as structure—not just text.
