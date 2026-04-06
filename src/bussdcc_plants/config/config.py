from dataclasses import dataclass, field, replace

from .settings import Settings


@dataclass(slots=True, frozen=True)
class Config:
    settings: Settings = field(
        metadata={
            "label": "Settings",
            "group": "General",
            "required": True,
        }
    )
