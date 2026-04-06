from bussdcc import Service, ContextProtocol

from ..library import load_default_seed_library


class SeedLibraryService(Service):
    name = "seed_library"

    def start(self, ctx: ContextProtocol) -> None:
        ctx.state.set("seed_library", load_default_seed_library())
