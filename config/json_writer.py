import json
from pathlib import Path


def write_into_json(json_path: Path, data: dict or list):
    with open(json_path, mode="w",encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
