from dataclasses import dataclass
from typing import Literal


@dataclass
class TriggerConfig:
    type: str


@dataclass(kw_only=True)
class Sensor(TriggerConfig):
    type: Literal["Sensor"] = "Sensor"
    interval: int


@dataclass(kw_only=True)
class Schedule(TriggerConfig):
    type: Literal["Schedule"] = "Schedule"
    cron: str


@dataclass
class Event(TriggerConfig):
    type: Literal["Event-Based"] = "Event-Based"
