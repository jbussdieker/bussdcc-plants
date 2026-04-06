from typing import Any
import secrets

from flask import redirect, url_for

from bussdcc import ContextProtocol
from bussdcc_framework.web import FlaskApp, WebInterface as Base

from .blueprints.settings import bp as settings_bp


class WebInterface(Base):
    def register_routes(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        app.secret_key = secrets.token_hex(32)

        @app.route("/")
        def index() -> Any:
            return redirect(url_for("bussdcc_plants_info.index"))

        app.register_blueprint(settings_bp)
