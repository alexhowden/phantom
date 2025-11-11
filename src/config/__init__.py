import os
import yaml
from pathlib import Path
from types import SimpleNamespace


def _to_namespace(d: dict) -> SimpleNamespace:
    '''Recursively convert a dict to a SimpleNamespace for dot access.'''
    if isinstance(d, dict):
        return SimpleNamespace(**{k: _to_namespace(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [_to_namespace(v) for v in d]
    return d


# load all YAML files
CONFIG_DIR = Path(__file__).parent
CONFIG = {}

for file in CONFIG_DIR.glob("*.yaml"):
    key = file.stem.lower()
    with open(file, "r", encoding="utf-8") as f:
        CONFIG[key] = yaml.safe_load(f) or {}

# convert nested dicts to attribute-accessible objects
CONFIG = _to_namespace(CONFIG)
