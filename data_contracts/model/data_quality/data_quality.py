import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import pandas as pd


class Action(str, Enum):
    BLOCK = "Bloqueio"
    WARN = "Aviso"


def validate_max_null_percentage(
    df: pd.DataFrame, column: str, percentage: float
) -> bool:
    """Verifica se a % de valores nulos em `column` não ultrapassa `percentage`."""
    null_percentage = df[column].isna().mean() * 100
    return null_percentage <= percentage


@dataclass
class CheckRule:
    description: str
    function: Callable[..., bool]
    column: str | list[str]
    action: Action = Action.BLOCK
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
            passed = rule.function(df, column=rule.column, **rule.params)
            results.append(CheckResult(rule=rule, passed=passed))
            if passed:
                continue
            if rule.action == Action.BLOCK:
                raise DataQualityCheckFailed(rule)
            warnings.warn(
                f"Check não-bloqueante falhou: {rule.description}", stacklevel=2
            )
        return results
