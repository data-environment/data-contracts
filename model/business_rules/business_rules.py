from dataclasses import dataclass


@dataclass
class Rule:
    name: str
    description: str


@dataclass
class BusinessRules:
    rules: list[Rule]
