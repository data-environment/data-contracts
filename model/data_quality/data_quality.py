from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class DataQuality:
    checks: dict[Callable[..., None], list[str] | dict[str, Any]]
