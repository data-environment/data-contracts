from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, constr

from data_contracts.model import (
    Api,
    BusinessRules,
    CaptureFrequency,
    CaptureMethod,
    Consumer,
    Contact,
    DataContract,
    DataExtraction,
    DataIngestion,
    DataQuality,
    DataSchema,
    DataSource,
    Distribution,
    Function,
    General,
    RedshiftIngestion,
    Rule,
    S3Ingestion,
    Schedule,
    Transformation,
    UpdateFrequency,
)


class AvenueFxSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    fx_date: date = Field(
        alias="fx.date",
        description="Data da operação de câmbio. Watermark da ingestão incremental.",
    )
    client_cpf: constr(pattern=r"^\d+$", max_length=11) = Field(
        alias="fx.client_cpf",
        description="CPF do cliente.",
        json_schema_extra={"sensitive": True},
    )
    client_email: str = Field(
        alias="fx.client_email",
        description="E-mail do cliente.",
        json_schema_extra={"sensitive": True},
    )
    client_name: str = Field(
        alias="fx.client_name",
        description="Nome completo do cliente.",
        json_schema_extra={"sensitive": True},
    )
    foreign_finder_email: str = Field(
        alias="fx.foreign_finder_email",
        description="E-mail do assessor vinculado ao cliente.",
        json_schema_extra={"sensitive": True},
    )
    foreign_finder_code: str = Field(
        alias="fx.foreign_finder_code",
        description="Código do assessor na plataforma Avenue.",
    )
    foreign_finder_name: str = Field(
        alias="fx.foreign_finder_name",
        description="Nome do assessor vinculado.",
        json_schema_extra={"sensitive": True},
    )
    office_cnpj: constr(pattern=r"^\d+$", max_length=14) = Field(
        alias="fx.office_cnpj",
        description="CNPJ do escritório do assessor.",
    )
    office_name: str = Field(alias="fx.office_name", description="Nome do escritório.")
    fx_id: str = Field(
        alias="fx.fx_id",
        description="Identificador único da operação de câmbio na Avenue.",
        json_schema_extra={"unique_key": True},
    )
    direction: str = Field(
        alias="fx.direction",
        description=(
            "Direção da operação de câmbio. Valores observados: EU, BU, UB, "
            "UE, BE. Sem Literal no model real — valores levantados via "
            "SELECT DISTINCT no DW (ver Observações Extras da doc)."
        ),
    )
    purpose: str = Field(
        alias="fx.purpose",
        description=(
            "Finalidade da operação de câmbio. Valores observados: "
            "InvestmentFunds, Investment, CurrencyExchange, Availability. "
            "Sem Literal no model real."
        ),
    )
    volume_brl: Decimal = Field(
        alias="fx.volume_brl", description="Volume da operação em BRL."
    )
    volume_usd: Decimal = Field(
        alias="fx.volume_usd", description="Volume da operação em USD."
    )


AVENUE_FX_CONTRACT = DataContract(
    General(
        display_name="Operações de Câmbio (FX) — Avenue",
        system_name="avenue_fx",
        pipeline_id="avenue_fx_job",
        description=(
            "Histórico de operações de câmbio (BR->US e US->BR) dos clientes "
            "Avenue, extraído da view `fx` da Looker API e persistido no "
            "datamart de alocação (`parceiro.avenue_fx`)."
        ),
        business_justification=(
            "Permite à equipe de Performance acompanhar o volume de captação "
            "e remessa de recursos por cliente e assessor. Tabela atualmente "
            "sem consumo ativo — ver Distribution."
        ),
        version=1,
        status="Active",
        tags=["parceiro", "avenue", "fx", "cambio"],
        cnpj_needed=False,
        approved_by=None,
        approved_at=None,
    ),
    DataSource(
        description=(
            "Avenue Analytics (Looker) — view `fx` do model " "`avenue_b2b_office_api`."
        ),
        update_frequency=UpdateFrequency.DAILY,
        owner=Contact(
            name="Avenue",
            contact_emails=["middle.b2b@avenue.us"],
        ),
    ),
    DataExtraction(
        description=(
            "Pipeline incremental. Extrai registros com `fx_date` entre "
            "MAX(fx_date)+1 (DW) e HOJE-1, filtrado diretamente na query "
            "Looker. O dia corrente é excluído por poder estar incompleto "
            "na origem."
        ),
        capture_frequency=CaptureFrequency.DAILY,
        capture_method=CaptureMethod.INCREMENTAL,
        extractor=Api(
            endpoint="https://avenueanalytics.cloud.looker.com/api/4.0/queries/run/json",
        ),
        details="Requisição HTTP POST ao endpoint da Looker API.",
        owner=Contact(
            name="Equipe de Dados",
            contact_emails=["gestaodedados@investsmart.com.br"],
        ),
    ),
    DataSchema(model=AvenueFxSchema),
    DataQuality(
        checks=[],
    ),
    DataIngestion(
        trigger=Schedule(cron="25 20 * * 1-5"),
        s3_ingestion=S3Ingestion(
            s3_path="parceiros/avenue/fx",
            s3_file="avenue_fx",
            inserter="avenue_fx_job",
        ),
        redshift_ingestion=RedshiftIngestion(
            redshift_table="avenue_fx",
            redshift_schema="parceiro",
            redshift_database="dw",
            redshift_write_mode="append",
        ),
    ),
    Distribution(
        consumers=[
            Consumer(
                type="Datamart",
                consumption_purpose=(
                    "Acompanhar volume de captação e remessa de recursos por "
                    "cliente e assessor (atualmente sem consumo ativo)."
                ),
                how=(
                    "Ainda sem consumo ativo — tabela disponibilizada em "
                    "`parceiro.avenue_fx` para consulta futura pelo "
                    "datamart de alocação."
                ),
                owner=Contact(
                    name="Equipe de Performance — Datamart de Alocação",
                    contact_emails=["performance.best@investsmart.com.br"],
                ),
                delivery_sla=None,
                delivery_deadline=time(3, 0),
            ),
        ],
    ),
    Transformation(
        functions=[
            Function(
                name="filter_current_day",
                description=(
                    "Exclui o dia corrente da extração — os dados do dia "
                    "ainda podem estar incompletos na origem."
                ),
            ),
        ]
    ),
    BusinessRules(
        rules=[
            Rule(
                name="incremental_watermark_fx_date",
                description=(
                    "Extração incremental baseada em `fx_date`: apenas "
                    "registros entre MAX(fx_date)+1 (DW) e HOJE-1 são "
                    "extraídos a cada execução."
                ),
            ),
        ],
    ),
)
