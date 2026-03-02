import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def extractStemFromCanvasFileField(file_field: str) -> str:
    file_field = file_field.replace("\\", "/")
    name = file_field.split("/")[-1]
    return name.rsplit(".", 1)[0]
