from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.poetry import Poetry

from poem_plugins.config import Config


class BasePlugin(ApplicationPlugin):
    def get_config(self, poetry: Poetry) -> Config:
        raw = poetry.pyproject.data.get("tool", {}).get("poem-plugins", {})
        return Config(**raw)
