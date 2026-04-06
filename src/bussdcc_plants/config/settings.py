from dataclasses import dataclass, field, replace
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Settings:
    name: str = field(
        metadata={
            "label": "Name",
            "group": "General",
            "required": True,
            "help": "Unique instance name.",
        }
    )

    something: dict[str, str] | None = field(
        default_factory=dict,
        metadata={
            "label": "Aliases",
            "group": "General",
            "key_meta": {
                "label": "Plant",
                "ref": {"kind": "plant", "type": "uuid", "protocol": "bussdcc-plants"},
                "required": True,
            },
        },
    )

    aliases: dict[str, UUID] | None = field(
        default_factory=dict,
        metadata={
            "label": "Aliases",
            "group": "General",
            "value_meta": {
                "label": "Plant",
                "ref": {"kind": "plant", "type": "uuid", "protocol": "bussdcc-plants"},
                "required": True,
            },
        },
    )

    favorites: list[UUID] | None = field(
        default_factory=list,
        metadata={
            "label": "Favorites",
            "group": "General",
            "item_meta": {
                "label": "Plant",
                "ref": {"kind": "plant", "type": "uuid", "protocol": "bussdcc-plants"},
                "required": True,
            },
        },
    )

    default_plant: UUID | None = field(
        default=None,
        metadata={
            "label": "Default Plant",
            "group": "General",
            "help": "Default plant selection.",
            "ref": {
                "kind": "plant",
                "type": "uuid",
                "protocol": "bussdcc-plants",
            },
        },
    )


def build_default_settings() -> Settings:
    return Settings(
        name="plants-1",
        default_plant=None,
    )
