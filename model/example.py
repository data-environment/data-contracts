from datetime import time
from decimal import Decimal

from pydantic import BaseModel, Field

from model import (
    CSV,
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


class OportunidadesVendaSchema(BaseModel):
    id_oportunidade: int = Field(
        description="Identificador único da oportunidade de venda.",
        # unique_key marca a(s) coluna(s) que formam a CHAVE DE NEGÓCIO do
        # dataset — não é necessariamente a mesma coisa que a PRIMARY KEY
        # física da tabela de destino (o Redshift pode ter seu próprio `id`
        # surrogate). `DataContract` usa essa marcação para sincronizar
        # automaticamente o check `check_no_duplicates` de DatasetQuality:
        # não é preciso (nem deve-se) declará-lo manualmente em
        # `dataset_quality.checks` quando a chave já está marcada aqui.
        json_schema_extra={"unique_key": True},
    )
    status_oportunidade: str = Field(
        description="Status atual da oportunidade de venda."
    )
    valor_venda: Decimal | None = Field(
        default=None, description="Valor monetário associado à oportunidade de venda."
    )
    data_criacao: str = Field(
        description="Data de criação da oportunidade, no formato YYYY-MM-DD."
    )
    documento_cliente: str | None = Field(
        default=None,
        description="CPF ou CNPJ do cliente associado à oportunidade.",
        # sensitive marca dado pessoal/PII sujeito à LGPD (CPF, e-mail, nome
        # de pessoa física etc). É INDEPENDENTE de unique_key: uma coluna
        # pode ser sensível sem ser chave, ser chave sem ser sensível, ou as
        # duas coisas ao mesmo tempo — cada flag existe para um consumidor
        # diferente (checagem de duplicidade x mascaramento de dados).
        json_schema_extra={"sensitive": True},
    )


# ---------------------------------------------------------------------------
# Inserter alternativo: SmartCheck (em vez de uma string simples)
#
# `S3Ingestion.inserter` aceita uma string (nome do job/step function que
# sobe o arquivo) OU um `SmartCheck`, usado quando o arquivo chega de um
# parceiro (CSV, XLSX, ...) e precisa ser validado contra um formato
# esperado antes de subir para o S3. O objeto abaixo é só para
# referência/documentação viva — não faz parte do `FILE_MODEL_EXAMPLE`
# construído mais adiante, que usa uma string simples como inserter.
# ---------------------------------------------------------------------------
CSV_FORMAT_EXAMPLE = CSV(separator=";", encoding="UTF-8", header=True)


FILE_MODEL_EXAMPLE = DataContract(
    General(
        display_name="Nome formatado que será exibido",
        system_name="nome_padrao_do_dado_para_os_sistemas",
        # Identificador do Job/DAG real que este contrato governa (ex.:
        # "avenue_fx_job", igual ao nome usado pelo Dagster) — o elo formal
        # entre o contrato e o pipeline de produção.
        pipeline_id="oportunidades_venda_job",
        description="Texto descritivo resumido sobre o dado, sua origem, propósito e outras informações relevantes.",
        business_justification="Esses dados são essenciais para análises no sistema etc...",
        # Versão do contrato — incremente sempre que um campo existente
        # mudar de forma incompatível (ex.: schema, chave única, SLA).
        version=1,
        # "Active" -> contrato vigente e sendo usado pelos pipelines.
        # "Inactive" -> contrato desativado (dataset descontinuado, ou
        # substituído por outro contrato), mantido só para histórico.
        status="Active",
        tags=["vendas", "comissoes"],
        cnpj_needed=False,
        # Preenchidos somente quando a Ficha de Validação correspondente é
        # assinada pela área de negócio responsável — até lá, ficam None.
        approved_by=None,
        approved_at=None,
    ),
    DataSource(
        description="Ex: Sistema que o parceiro tal disponibiliza os dados, ou um relatório específico, ou uma API etc...",
        update_frequency=UpdateFrequency.DAILY,
        owner=Contact(
            name="Ex: Performance, Comissões, etc...",
            contact_emails=["engenharia@empresa.com", "engenharia2@empresa.com"],
        ),
    ),
    DataExtraction(
        description="Ex: Relatório de tal extraído manualmente de tal sistema, ou via API, ou extraído de um banco de dados via query SQL etc...",
        capture_frequency=CaptureFrequency.DAILY,
        capture_method=CaptureMethod.INCREMENTAL,
        extractor=Api(
            endpoint="https://api.exemplo.com.br/v1/oportunidades",
        ),
        owner=Contact(
            name="Ex: Performance, Comissões, etc...",
            contact_emails=["engenharia@empresa.com", "engenharia2@empresa.com"],
        ),
    ),
    DataSchema(model=OportunidadesVendaSchema),
    DataQuality(
        checks={},
    ),
    DataIngestion(
        trigger=Schedule(cron="0 3 * * *"),
        s3_ingestion=S3Ingestion(
            s3_path="string/tal/caminho",
            s3_file="exemplo.xlsx",
            inserter="nome_do_job_ou_step_function_que_sobe_o_arquivo",
        ),
        redshift_ingestion=RedshiftIngestion(
            redshift_table="tabela",
            redshift_schema="schema",
            redshift_database="dw",
            redshift_write_mode="upsert",
        ),
    ),
    Distribution(
        consumers=[
            Consumer(
                type="Datamart",
                consumption_purpose="Medir dados de vendas",
                how="Ex: Consumido via view materializada no Redshift",
                delivery_sla=3,
                owner=Contact(
                    name="Ex: Performance",
                    contact_emails=[
                        "engenharia@empresa.com",
                        "engenharia2@empresa.com",
                    ],
                ),
            ),
            Consumer(
                type="Google Sheets",
                consumption_purpose="Dados de colaboradores para a botmaker",
                how="Ex: Planilha atualizada via export automático",
                delivery_deadline=time(3, 0),
                owner=Contact(
                    name="Ex: Processos",
                    contact_emails=[
                        "engenharia@empresa.com",
                        "engenharia2@empresa.com",
                    ],
                ),
            ),
        ],
    ),
    Transformation(
        functions=[
            Function(
                name="filter_cancelled",
                description="Exclui oportunidades canceladas do dataset.",
            ),
        ]
    ),
    BusinessRules(
        rules=[
            Rule(
                name="filter_cancelled",
                description="Exclui oportunidades canceladas do dataset.",
            ),
            Rule(
                name="M+1",
                description="Os colaboradores são pagos no mês seguinte ao da venda, então só consideramos as vendas até o mês anterior para calcular a comissão etc...",
            ),
        ],
    ),
)
