from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


def check_no_duplicates(columns: list[str]) -> None:
    """Verifica duplicidade nos valores da(s) coluna(s) de chave única do dataset.

    Usado como chave em `DataQuality.checks` — não é chamado diretamente por
    este pacote, apenas serve de identidade para o motor de execução que roda
    os checks. `DataContract` sincroniza este check automaticamente a partir
    de `DataSchema.unique_key_columns()`.
    """


@dataclass
class DataQuality:
    checks: dict[Callable[..., None], list[str] | dict[str, Any]]
