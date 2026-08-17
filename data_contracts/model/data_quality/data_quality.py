import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import pandas as pd
from sqlalchemy import text

from data_contracts.db.redshift import get_redshift_engine


class Action(str, Enum):
    BLOCK = "Bloqueio"
    WARN = "Aviso"


def validate_max_null_percentage(df: pd.DataFrame, column: str, percentage: float) -> bool:
    """Verifica se a % de valores nulos em `column` não ultrapassa `percentage`."""
    null_percentage = df[column].isna().mean() * 100
    return null_percentage <= percentage


def validate_value_range(
    df: pd.DataFrame,
    column: str,
    redshift_schema: str,
    redshift_table: str,
    date_column: str,
    variation_multiplier: float = 2,
    redshift_column: str | None = None,
) -> bool:
    """Verifica se a soma atual de `column` está dentro do range esperado.

    teto = PL do mês anterior * (1 + maior variação mensal dos últimos 12 meses * variation_multiplier)
    piso = PL do mês anterior * (1 - maior variação mensal dos últimos 12 meses * variation_multiplier)

    O histórico mensal é buscado no Redshift, na tabela que o próprio
    contrato ingere (`RedshiftIngestion.redshift_schema`/`redshift_table`),
    já que o dado do mês corrente ainda não foi carregado lá.
    """
    engine = get_redshift_engine()
    query = text(
        f"""
        SELECT DATE_TRUNC('month', {date_column}) AS mes,
               SUM({redshift_column or column}) AS total
        FROM {redshift_schema}.{redshift_table}
        GROUP BY 1
        ORDER BY 1 DESC
        LIMIT 13
        """
    )
    history = pd.read_sql(query, engine).sort_values("mes")["total"]

    previous_pl = history.iloc[-1]
    max_variation = history.pct_change().abs().max()
    ceiling = previous_pl * (1 + max_variation * variation_multiplier)
    floor = previous_pl * (1 - max_variation * variation_multiplier)

    current_value = df[column].sum()
    return floor <= current_value <= ceiling


@dataclass
class CheckRule:
    description: str
    function: Callable[..., bool]
    column: str | list[str]
    action: Action = Action.BLOCK
    percentage: float | None = None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class CheckResult:
    rule: CheckRule
    passed: bool


class DataQualityCheckFailed(Exception):
    def __init__(self, rule: CheckRule) -> None:
        self.rule = rule
        super().__init__(f"Check bloqueante falhou: {rule.description}")


@dataclass
class DataQuality:
    checks: list[CheckRule]

    def run(self, df: pd.DataFrame) -> list[CheckResult]:
        """Executa cada CheckRule contra `df`.

        Levanta `DataQualityCheckFailed` assim que um check com
        `action=Action.BLOCK` falha. Checks com `action=Action.WARN` que
        falham apenas emitem um `warnings.warn`, sem interromper a execução.
        """
        results = []
        for rule in self.checks:
            kwargs: dict[str, Any] = dict(rule.params)
            if rule.percentage is not None:
                kwargs["percentage"] = rule.percentage
            passed = rule.function(df, column=rule.column, **kwargs)
            results.append(CheckResult(rule=rule, passed=passed))
            if passed:
                continue
            if rule.action == Action.BLOCK:
                raise DataQualityCheckFailed(rule)
            warnings.warn(f"Check não-bloqueante falhou: {rule.description}", stacklevel=2)
        return results
