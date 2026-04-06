from __future__ import annotations

from dataclasses import Field, dataclass, field
from typing import Any, Literal, TypeVar, overload
from uuid import UUID

Lifecycle = Literal["annual", "biennial", "perennial"]
DistanceUnit = Literal["in"]
PlantingMethod = Literal["press", "cover_lightly", "surface", "trench"]

T = TypeVar("T")


@overload
def config_field(
    *,
    doc: str,
    units: str | None = None,
    examples: tuple[object, ...] | None = None,
    nullable: bool = False,
) -> Any: ...


@overload
def config_field(
    *,
    doc: str,
    units: str | None = None,
    examples: tuple[object, ...] | None = None,
    nullable: bool = False,
    default: T,
) -> T: ...


@overload
def config_field(
    *,
    doc: str,
    units: str | None = None,
    examples: tuple[object, ...] | None = None,
    nullable: bool = False,
    default_factory: Any,
) -> Any: ...


def config_field(
    *,
    doc: str,
    units: str | None = None,
    examples: tuple[object, ...] | None = None,
    nullable: bool = False,
    default: Any = ...,
    default_factory: Any = ...,
) -> Any:
    metadata: dict[str, object] = {"doc": doc}

    if units is not None:
        metadata["units"] = units
    if examples is not None:
        metadata["examples"] = examples
    if nullable:
        metadata["nullable"] = True

    if default is not ... and default_factory is not ...:
        msg = "config_field() cannot specify both default and default_factory"
        raise TypeError(msg)

    if default is not ...:
        return field(default=default, metadata=metadata)

    if default_factory is not ...:
        return field(default_factory=default_factory, metadata=metadata)

    return field(metadata=metadata)


@dataclass(slots=True, kw_only=True)
class Range:
    min: float = config_field(
        doc="Lower bound of the range.",
        examples=(0.25, 4.0, 18.0),
    )
    max: float = config_field(
        doc="Upper bound of the range.",
        examples=(0.25, 8.0, 24.0),
    )


@dataclass(slots=True, kw_only=True)
class DistanceRange:
    min: float = config_field(
        doc="Minimum distance.",
        units="in",
        examples=(0.0, 0.25, 12.0),
    )
    max: float = config_field(
        doc="Maximum distance.",
        units="in",
        examples=(0.125, 1.0, 36.0),
    )
    unit: DistanceUnit = config_field(
        doc="Unit of measure for the distance range.",
        examples=("in",),
    )


@dataclass(slots=True, kw_only=True)
class PlantingDepth:
    min: float = config_field(
        doc="Minimum planting depth.",
        units="in",
        examples=(0.0, 0.25, 1.0),
    )
    max: float = config_field(
        doc="Maximum planting depth.",
        units="in",
        examples=(0.0, 0.5, 4.0),
    )
    unit: DistanceUnit = config_field(
        doc="Unit of measure for planting depth.",
        examples=("in",),
    )
    method: PlantingMethod | None = config_field(
        doc="Optional planting method modifier.",
        examples=("press", "surface", "trench"),
        nullable=True,
        default=None,
    )
    notes: str | None = config_field(
        doc="Optional planting notes.",
        nullable=True,
        default=None,
    )


@dataclass(slots=True, kw_only=True)
class Spacing:
    plant: DistanceRange = config_field(
        doc="Recommended spacing between plants.",
    )
    row: DistanceRange | None = config_field(
        doc="Recommended spacing between rows.",
        nullable=True,
        default=None,
    )


@dataclass(slots=True, kw_only=True)
class Hydration:
    target: Range = config_field(
        doc="Target hydration range expressed as fraction of field capacity.",
        examples=((0.55, 0.85),),
    )


@dataclass(slots=True, kw_only=True)
class Hardiness:
    min: int = config_field(
        doc="Minimum USDA hardiness zone.",
        examples=(3, 5, 9),
    )
    max: int = config_field(
        doc="Maximum USDA hardiness zone.",
        examples=(9, 10, 11),
    )


@dataclass(slots=True, kw_only=True)
class Taxonomy:
    genus: str = config_field(
        doc="Botanical genus.",
        examples=("Ocimum", "Mentha", "Solanum"),
    )
    species: str = config_field(
        doc="Botanical species epithet or hybrid notation.",
        examples=("basilicum", "× piperita", "lycopersicum"),
    )


@dataclass(frozen=True, slots=True)
class PlantName:
    crop_name: str
    variety_name: str | None = None
    qualifiers: tuple[
        Literal[
            "organic",
            "hybrid",
            "heirloom",
            "cover-crop",
            "everbearing",
        ],
        ...,
    ] = field(default_factory=tuple)
    source_label: str | None = None

    @property
    def display_name(self) -> str:
        if self.variety_name:
            return f"{self.variety_name} {self.crop_name}"
        return self.crop_name

    @property
    def full_name(self) -> str:
        base = self.display_name
        if self.qualifiers:
            q = ", ".join(q.title() for q in self.qualifiers)
            return f"{base} ({q})"
        return base

    @property
    def sort_name(self) -> str:
        if self.variety_name:
            return f"{self.crop_name} — {self.variety_name}"
        return self.crop_name


@dataclass(slots=True, kw_only=True)
class PlantSpec:
    name: PlantName = config_field(doc="Structured plant naming information.")
    url: str | None = config_field(
        doc="Optional source or product URL.",
        nullable=True,
        default=None,
    )
    planting_depth: PlantingDepth = config_field(doc="Planting depth recommendation.")
    botanical_lifecycle: Lifecycle = config_field(
        doc="Lifecycle in botanical terms.",
        examples=("annual", "biennial", "perennial"),
    )
    cultivation_lifecycle: Lifecycle = config_field(
        doc="Lifecycle in cultivation terms.",
        examples=("annual", "biennial", "perennial"),
    )
    spacing: Spacing = config_field(
        doc="Plant and optional row spacing recommendations."
    )
    hydration: Hydration = config_field(doc="Hydration targets for the plant.")
    hardiness: Hardiness = config_field(doc="USDA hardiness range.")
    taxonomy: Taxonomy = config_field(doc="Botanical taxonomy.")


@dataclass(slots=True, kw_only=True)
class SeedLibrary:
    plants: dict[UUID, PlantSpec] = config_field(
        doc="Plant specifications keyed by UUID.",
        default_factory=dict,
    )
