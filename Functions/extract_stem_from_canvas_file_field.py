# BundleTools.py
from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# ============================================================
# 1) Canvas -> list of function names  (optional utilities)
# ============================================================

def extract_stem_from_canvas_file_field(file_field: str) -> str:
    file_field = file_field.replace("\\", "/")
    name = file_field.split("/")[-1]
    return name.rsplit(".", 1)[0]
