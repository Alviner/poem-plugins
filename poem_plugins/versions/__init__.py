from cleo.events.console_events import COMMAND
from poetry.console.application import Application

from poem_plugins.base import BasePlugin
from poem_plugins.versions.dispatcher import VersionDispatcher


class VersionPlugin(BasePlugin):
    def activate(self, application: Application) -> None:
        if not application.event_dispatcher:
            return

        config = self.get_config(application.poetry)

        version_dispatcher = VersionDispatcher.factory(
            config=config,
        )
        application.event_dispatcher.add_listener(
            COMMAND, version_dispatcher,
        )
