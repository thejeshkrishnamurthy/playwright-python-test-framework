import json
from pathlib import Path
from typing import Any


def load_json(file_path: str) -> Any:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Test data file was not found: {file_path}"
        )

    with path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        return json.load(file)