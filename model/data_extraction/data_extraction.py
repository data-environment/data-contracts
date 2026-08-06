from dataclasses import dataclass
from enum import Enum
from typing import Literal

from ..general.general import Contact


class CaptureFrequency(str, Enum):
    REAL_TIME = "Tempo real"
    INTRADAY = "Intradiária"
    DAILY = "Diária"
    WEEKLY = "Semanal"
    BIWEEKLY = "Quinzenal"
    MONTHLY = "Mensal"
    QUARTERLY = "Trimestral"
    ON_DEMAND = "Sob demanda"


class CaptureMethod(str, Enum):
    FULL_LOAD = "Full Load"
    INCREMENTAL = "Incremental (Delta)"
    CDC = "CDC (Change Data Capture)"
    APPEND_ONLY = "Append Only"
    SNAPSHOT = "Snapshot"
    UPSERT = "Upsert (Merge)"
    MONTHLY_INCREMENTAL = "Incremental Mensal"


#####################
# EXTRACTION CONFIG #
#####################


@dataclass
class ExtractionConfig:
    type: str


@dataclass(kw_only=True)
class Api(ExtractionConfig):
    type: Literal["API"] = "API"
    endpoint: str


@dataclass(kw_only=True)
class Manual(ExtractionConfig):
    type: Literal["Manual"] = "Manual"
    description: str


@dataclass
class DataExtraction:
    description: str
    capture_frequency: CaptureFrequency
    capture_method: CaptureMethod
    extractor: ExtractionConfig
    owner: Contact
    details: str | None = None
