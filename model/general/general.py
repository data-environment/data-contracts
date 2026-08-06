from dataclasses import dataclass
from datetime import date
from typing import Literal

from ..business_rules.business_rules import BusinessRules
from ..data_extraction.data_extraction import DataExtraction
from ..data_ingestion.data_ingestion import DataIngestion
from ..data_quality.data_quality import DataQuality, check_no_duplicates
from ..data_schema.data_schema import DataSchema
from ..data_source.data_source import DataSource
from ..distribution.distribution import Distribution
from ..transformation.transformation import Transformation


@dataclass
class General:
    display_name: str
    system_name: str
    pipeline_id: str
    description: str
    business_justification: str
    version: int
    status: Literal["Active", "Inactive"] = "Active"
    tags: list[str] | None = None
    cnpj_needed: bool | None = False
    approved_by: str | None = None
    approved_at: date | None = None


@dataclass
class DataContract:
    general: General
    data_source: DataSource
    data_extraction: DataExtraction
    schema: DataSchema
    data_quality: DataQuality
    data_ingestion: DataIngestion
    distribution: Distribution
    transformation: Transformation
    business_rules: BusinessRules

    def __post_init__(self) -> None:
        unique_key_columns = self.schema.unique_key_columns()
        if not unique_key_columns:
            return
        if check_no_duplicates in self.data_quality.checks:
            raise ValueError(
                "check_no_duplicates é sincronizado automaticamente a partir das "
                "colunas unique_key do DataSchema — não declare em DataQuality.checks."
            )
        self.data_quality.checks[check_no_duplicates] = unique_key_columns
