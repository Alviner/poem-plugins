from typing import NamedTuple, Optional


class Version(NamedTuple):
    major: int
    minor: int
    patch: int
    commit: Optional[str] = None

    def __str__(self) -> str:
        if not self.commit:
            return f"{self.major}.{self.minor}.{self.patch}"
        return f"{self.major}.{self.minor}.{self.patch}+g{self.commit}"
