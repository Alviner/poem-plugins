import abc
from typing import Any, Mapping

from poetry.poetry import Poetry

from poem_plugins.config.base import BaseConfig


class BaseDispatcher(abc.ABC):
    @abc.abstractmethod
    def get_config(self, poetry: Poetry) -> BaseConfig:
        raise NotImplementedError

    def get_raw_config(self, poetry: Poetry) -> Mapping[str, Any]:
        return poetry.pyproject.data.get("tool", {}).get("poem-plugins", {})
