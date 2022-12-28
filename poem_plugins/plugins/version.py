from cleo.events.console_events import COMMAND
from poetry.console.application import Application
from poetry.poetry import Poetry

from poem_plugins.config import VersionConfig
from poem_plugins.dispatchers.version import VersionDispatcher
from poem_plugins.plugins.base import BasePlugin


class VersionPlugin(BasePlugin):
    def get_config(self, poetry: Poetry) -> VersionConfig:
        base = super().get_raw_config(poetry)
        return VersionConfig.fabric(base)

    def activate(self, application: Application) -> None:
        if not application.event_dispatcher:
            return

        try:
            config = self.get_config(application.poetry)
        except Exception as exc:
            io = application.create_io()
            io.write_line(
                "<b>poem-plugins</b>: "
                f"Cannot load version config, skipping: {exc}",
            )
            return

        if not config.provider:
            return
        version_dispatcher = VersionDispatcher.factory(
            config=config,
        )
        application.event_dispatcher.add_listener(
            COMMAND, version_dispatcher,
        )
