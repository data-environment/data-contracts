from dataclasses import dataclass
from typing import Literal

from .file_format import FileFormat
from .trigger import TriggerConfig


@dataclass
class InserterConfig:
    type: str


@dataclass(kw_only=True)
class SmartCheck(InserterConfig):
    type: Literal["SmartCheck"] = "SmartCheck"
    model_link: str
    expected_file_format: FileFormat


BUCKET_BRONZE = "bronze-us-east-1-060791893263"


@dataclass(kw_only=True)
class S3Ingestion:
    s3_bucket: str = BUCKET_BRONZE
    s3_path: str
    s3_file: str
    inserter: str | InserterConfig


@dataclass
class RedshiftIngestion:
    redshift_table: str
    redshift_schema: str
    redshift_database: str
    redshift_write_mode: Literal["overwrite", "append", "upsert", "merge", "insert"]


@dataclass
class DataIngestion:
    trigger: TriggerConfig
    s3_ingestion: S3Ingestion
    redshift_ingestion: RedshiftIngestion
