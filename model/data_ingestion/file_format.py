from dataclasses import dataclass
from typing import Literal


@dataclass
class FileFormat:
    type: str


@dataclass
class CSV(FileFormat):
    type: Literal["CSV"] = "CSV"
    separator: str = ","
    encoding: str = "UTF-8"
    header: bool = True
    quote_char: str = '"'
    escape_char: str | None = None
    null_value: str | None = None


@dataclass
class XLSX(FileFormat):
    type: Literal["XLSX"] = "XLSX"
    sheet_name: str = "Sheet1"
    header_row: int = 1
    encoding: str = "UTF-8"
