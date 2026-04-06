from typing import Any
from uuid import UUID

from flask import Blueprint, render_template

from bussdcc import ContextProtocol
from bussdcc_framework.web import BaseWebPlugin, FlaskApp, WebPlugin

from ....model import PlantSpec


def build_grouped_plants(
    plants: dict[UUID, PlantSpec],
) -> list[tuple[str, list[tuple[UUID, PlantSpec]]]]:
    grouped: dict[str, list[tuple[UUID, PlantSpec]]] = {}

    for uuid, plant in sorted(
        plants.items(),
        key=lambda item: (
            item[1].name.crop_name.lower(),
            item[1].name.sort_name.lower(),
        ),
    ):
        crop_name = plant.name.crop_name
        grouped.setdefault(crop_name, []).append((uuid, plant))

    return list(grouped.items())


class PlantsInfoPlugin(BaseWebPlugin):
    name = "plants-info"

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        bp = Blueprint(
            "bussdcc_plants_info",
            __name__,
            url_prefix="/plants/info",
            template_folder="templates",
        )

        @bp.route("/")
        def index() -> Any:
            library = ctx.state.get("seed_library")
            plant_groups = build_grouped_plants(library.plants)
            return render_template(
                "bussdcc_plants/info/index.html",
                plant_groups=plant_groups,
            )

        @bp.route("/show/<uuid>")
        def show(uuid: str) -> Any:
            library = ctx.state.get("seed_library")
            plant_groups = build_grouped_plants(library.plants)

            try:
                plant_uuid = UUID(uuid)
            except ValueError:
                return "Plant not found", 404

            if plant_uuid not in library.plants:
                return "Plant not found", 404

            return render_template(
                "bussdcc_plants/info/show.html",
                plant_groups=plant_groups,
                id=plant_uuid,
                plant=library.plants[plant_uuid],
            )

        app.register_blueprint(bp)


plugin: WebPlugin = PlantsInfoPlugin()
