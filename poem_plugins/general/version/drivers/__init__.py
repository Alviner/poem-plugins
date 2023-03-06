import abc
from typing import Optional

from poem_plugins.config import QuoteEnum
from poem_plugins.general.version import Version


class IVervsionDriver(abc.ABC):
    @abc.abstractmethod
    def get_version(self) -> Version:
        raise NotImplementedError

    @abc.abstractmethod
    def render_version_file(
        self, version: Version, quote: Optional[QuoteEnum] = None,
    ) -> str:
        raise NotImplementedError
