from dataclasses import dataclass
from datetime import time

from ..general.contact import Contact


@dataclass
class Consumer:
    type: str
    consumption_purpose: str
    how: str
    owner: Contact
    # SLA relativo: prazo em dias corridos após a geração/extração do dado,
    # para consumidores cujo prazo é "N dias depois". Deixe None quando o
    # SLA real for um horário fixo (use `delivery_deadline` nesse caso) ou
    # quando ainda não houver SLA formalmente definido pelo negócio.
    delivery_sla: int | time | str | None = None
    # SLA absoluto: horário do dia em que o dado precisa estar disponível
    # (ex.: "disponível até as 03h00"). Um `Consumer` pode usar
    # `delivery_sla`, `delivery_deadline`, os dois, ou nenhum (SLA ainda não
    # definido) — mas não invente um valor placeholder em nenhum dos dois só
    # para preencher o campo.
    delivery_deadline: int | time | str | None = None


@dataclass
class Distribution:
    consumers: list[Consumer]
