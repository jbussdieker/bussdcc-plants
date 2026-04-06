from bussdcc_framework.interface.web.formtree.types import FieldOption
from bussdcc_framework.metadata import FieldRef

from ....model import SeedLibrary


class PlantRefResolver:
    def __init__(self, library: SeedLibrary) -> None:
        self.library = library

    def resolve(self, ref: FieldRef, field_type: object) -> list[FieldOption] | None:
        if ref.kind == "plant":
            return [
                FieldOption(value=str(uuid), label=plant.name.display_name)
                for uuid, plant in sorted(
                    self.library.plants.items(),
                    key=lambda item: item[1].name.sort_name,
                )
            ]

        return None
