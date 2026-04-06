from importlib import resources
import json
from pathlib import Path
from typing import cast

from bussdcc_framework.codec import load_value

from .model import SeedLibrary


def load_seed_library(file: str | Path) -> SeedLibrary:
    file = Path(file)
    with file.open("r", encoding="utf-8") as f:
        data: object = json.load(f)
    return cast(SeedLibrary, load_value(SeedLibrary, data))


def load_default_seed_library() -> SeedLibrary:
    with (
        resources.files("bussdcc_plants.data")
        .joinpath("seeds.json")
        .open("r", encoding="utf-8") as f
    ):
        data: object = json.load(f)
    return cast(SeedLibrary, load_value(SeedLibrary, data))
