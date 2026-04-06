from bussdcc import Service, ContextProtocol, Event, Message

from ..config import ConfigStore, Config
from .. import message


class ConfigService(Service):
    name = "config"

    def __init__(self, data_dir: str) -> None:
        self._data_dir = data_dir

    def _save_config(self, ctx: ContextProtocol) -> None:
        settings = ctx.state.get("settings")

        if settings is None:
            return

        self.cs.data = Config(
            settings=settings,
        )
        self.cs.save()

        ctx.emit(message.ConfigSaved())

    def start(self, ctx: ContextProtocol) -> None:
        self.cs = ConfigStore(f"{self._data_dir}/config.json")
        if self.cs.data is None:
            return

        ctx.emit(message.SettingsReplaced(self.cs.data.settings))

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None:
        payload = evt.payload

        if isinstance(payload, message.ConfigChanged):
            self._save_config(ctx)
            return

    def stop(self, ctx: ContextProtocol) -> None:
        self._save_config(ctx)
