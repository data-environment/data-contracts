from dataclasses import dataclass


@dataclass
class Function:
    name: str
    description: str


@dataclass
class Transformation:
    functions: list[Function]
