from dataclasses import dataclass
from enum import Enum

from ..general.contact import Contact


class UpdateFrequency(str, Enum):
    REAL_TIME = "Tempo real"
    INTRADAY = "Intradiária"
    DAILY = "Diária"
    WEEKLY = "Semanal"
    BIWEEKLY = "Quinzenal"
    MONTHLY = "Mensal"
    QUARTERLY = "Trimestral"
    SEMIANNUAL = "Semestral"
    ANNUAL = "Anual"
    ON_DEMAND = "Sob demanda"


@dataclass
class DataSource:
    description: str
    update_frequency: UpdateFrequency | str
    owner: Contact
    details: str | None = None
