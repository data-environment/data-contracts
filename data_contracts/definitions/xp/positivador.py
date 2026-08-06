from decimal import Decimal

from pydantic import BaseModel, Field

from data_contracts.model import (
    CSV,
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
    Manual,
    RedshiftIngestion,
    Rule,
    S3Ingestion,
    Sensor,
    SmartCheck,
    Transformation,
)


class PositivadorSchema(BaseModel):
    model_config = {"populate_by_name": True}

    cod_xp_assessor: str = Field(
        alias="Assessor",
        description="Código do assessor XP responsável pelo cliente.",
    )
    cod_xp_cliente: str = Field(
        alias="Cód_do_Cliente",
        description="Código do cliente na XP.",
    )
    profissao: str | None = Field(
        default=None,
        alias="Profissão",
        description="Profissão do cliente. Vazio para clientes Pessoa Jurídica.",
    )
    sexo: str | None = Field(
        default=None,
        alias="Sexo",
        description="Sexo do cliente. Vazio para clientes Pessoa Jurídica.",
    )
    dt_cadastro: str = Field(
        alias="Data_de_Cadastro",
        description="Data de cadastro do cliente, no formato YYYY-MM-DD.",
    )
    segundo_aporte: str | None = Field(
        default=None,
        alias="Fez_Segundo_Aporte_",
        description="Indica se o cliente fez o segundo aporte.",
    )
    dt_nascimento: str | None = Field(
        default=None,
        alias="Data_de_Nascimento",
        description="Data de nascimento do cliente, no formato YYYY-MM-DD. Vazio para clientes Pessoa Jurídica.",
    )
    status: str | None = Field(
        default=None, alias="Status", description="Status atual do cliente."
    )
    ativou_m: str | None = Field(
        default=None,
        alias="Ativou_em_M_",
        description="Indica se o cliente ativou a conta no mês.",
    )
    evadiu_m: str | None = Field(
        default=None,
        alias="Evadiu_em_M_",
        description="Indica se o cliente evadiu a conta no mês.",
    )
    operou_bolsa: str | None = Field(
        default=None,
        alias="Operou_Bolsa_",
        description="Indica se o cliente operou bolsa no mês.",
    )
    operou_fundo: str | None = Field(
        default=None,
        alias="Operou_Fundo_",
        description="Indica se o cliente operou fundo no mês.",
    )
    operou_renda_fixa: str | None = Field(
        default=None,
        alias="Operou_Renda_Fixa_",
        description="Indica se o cliente operou renda fixa no mês.",
    )
    Aplicacao_Financeira_Declarada: Decimal | None = Field(
        default=None,
        alias="Aplicação_Financeira_Declarada_Ajustada",
        description="Aplicação financeira declarada e ajustada do cliente.",
    )
    vlr_receita_mes: Decimal | None = Field(
        default=None,
        alias="Receita_no_Mês",
        description="Receita total gerada pelo cliente no mês.",
    )
    vlr_receita_bovespa: Decimal | None = Field(
        default=None,
        alias="Receita_Bovespa",
        description="Receita gerada por operações de bolsa (Bovespa).",
    )
    vlr_receita_futuros: Decimal | None = Field(
        default=None,
        alias="Receita_Futuros",
        description="Receita gerada por operações de futuros.",
    )
    vlr_receita_rf_bancarios: Decimal | None = Field(
        default=None,
        alias="Receita_RF_Bancários",
        description="Receita gerada por renda fixa bancária.",
    )
    vlr_receita_rf_privados: Decimal | None = Field(
        default=None,
        alias="Receita_RF_Privados",
        description="Receita gerada por renda fixa privada.",
    )
    vlr_receita_rf_publicos: Decimal | None = Field(
        default=None,
        alias="Receita_RF_Públicos",
        description="Receita gerada por renda fixa pública.",
    )
    vlr_captacao_bruta_m: Decimal | None = Field(
        default=None,
        alias="Captação_Bruta_em_M",
        description="Captação bruta do cliente no mês.",
    )
    vlr_resgate_m: Decimal | None = Field(
        default=None,
        alias="Resgate_em_M",
        description="Valor resgatado pelo cliente no mês.",
    )
    vlr_captacao_liquida_m: Decimal | None = Field(
        default=None,
        alias="Captação_Líquida_em_M1",
        description="Captação líquida do cliente no mês.",
    )
    vlr_captacao_ted: Decimal | None = Field(
        default=None, alias="Captação_TED", description="Captação via TED."
    )
    vlr_captacao_st: Decimal | None = Field(
        default=None, alias="Captação_ST", description="Captação via ST."
    )
    vlr_captacao_ota: Decimal | None = Field(
        default=None, alias="Captação_OTA", description="Captação via OTA."
    )
    vlr_captacao_rf: Decimal | None = Field(
        default=None, alias="Captação_RF", description="Captação em renda fixa."
    )
    vlr_captacao_td: Decimal | None = Field(
        default=None,
        alias="Captação_TD",
        description="Captação via Tesouro Direto.",
    )
    vlr_captacao_prev: Decimal | None = Field(
        default=None, alias="Captação_PREV", description="Captação em previdência."
    )
    vlr_net_m: Decimal | None = Field(
        default=None,
        alias="Net_Em_M1",
        description="Net total do cliente no mês (M).",
    )
    vlr_net_renda_fixa: Decimal | None = Field(
        default=None, alias="Net_Renda_Fixa", description="Net em renda fixa."
    )
    vlr_net_fundos_imobiliarios: Decimal | None = Field(
        default=None,
        alias="Net_Fundos_Imobiliários",
        description="Net em fundos imobiliários.",
    )
    vlr_net_renda_variavel: Decimal | None = Field(
        default=None,
        alias="Net_Renda_Variável",
        description="Net em renda variável.",
    )
    vlr_net_fundos: Decimal | None = Field(
        default=None, alias="Net_Fundos", description="Net em fundos."
    )
    vlr_net_financeiro: Decimal | None = Field(
        default=None, alias="Net_Financeiro", description="Net financeiro total."
    )
    vlr_net_previdencia: Decimal | None = Field(
        default=None, alias="Net_Previdência", description="Net em previdência."
    )
    vlr_net_outros: Decimal | None = Field(
        default=None, alias="Net_Outros", description="Net em outros produtos."
    )
    vlr_receita_aluguel: Decimal | None = Field(
        default=None,
        alias="Receita_Aluguel",
        description="Receita gerada por aluguel de ativos.",
    )
    vlr_receita_complemento_pacote_corretagem: Decimal | None = Field(
        default=None,
        alias="Receita_Complemento_Pacote_Corretagem",
        description="Receita complementar do pacote de corretagem.",
    )
    tipo_pessoa: str = Field(
        alias="Tipo_Pessoa",
        description="Tipo de pessoa do cliente: Física ou Jurídica.",
    )
    dt_posicao: str = Field(
        alias="Data_Atualização",
        description="Data de atualização da posição, no formato YYYY-MM-DD.",
    )


POSITIVADOR = DataContract(
    General(
        display_name="XP Positivador",
        system_name="xp_positivador",
        pipeline_id="xp_positivador_job",
        description="Relatório extraído da XP que contém informações sobre conta dos clientes, vinculadas a assessores, e seu net_m.",
        business_justification="Controle de custódia a nivel de cliente. Identificar segmento de cliente. Identificar taxa de ativação de contas. Complementar à Diversificação.",
        version=1,
        status="Active",
        tags=["xp"],
        cnpj_needed=False,
        approved_by=None,
        approved_at=None,
    ),
    DataSource(
        description="Hub da XP",
        update_frequency="D-2",
        owner=Contact(
            name="XP",
            contact_emails=[],
        ),
    ),
    DataExtraction(
        description="Relatório do Positivador extraído manualmente do Hub da XP.",
        capture_frequency=CaptureFrequency.DAILY,
        capture_method=CaptureMethod.MONTHLY_INCREMENTAL,
        extractor=Manual(
            description="Extraído manualmente do Hub da XP.",
        ),
        owner=Contact(
            name="Performance",
            contact_emails=["performance.best@investsmart.com.br"],
        ),
    ),
    DataSchema(model=PositivadorSchema),
    DataQuality(
        checks={
            # check_sum_range: {
            #     "column": "Net_Em_M1",
            #     "expected_sum": 31_000_000_000,
            #     "tolerance_warning": 0.2,  # passa com aviso
            #     "tolerance_block": 0.5,  # bloqueia voce esta maluco
            # },
        },
    ),
    DataIngestion(
        trigger=Sensor(interval=5400),
        s3_ingestion=S3Ingestion(
            s3_path="investsmart/xp_inc/positivador",
            s3_file="positivador.csv",
            inserter=SmartCheck(
                model_link="https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Finvestsmartxp-assets.s3.us-east-1.amazonaws.com%2Fmodelos_smartcheck%2Fmodelo_positivador.xlsx&wdOrigin=BROWSELINK",
                expected_file_format=CSV(
                    separator=",",
                    encoding="utf-8",
                ),
            ),
        ),
        redshift_ingestion=RedshiftIngestion(
            redshift_table="positivador",
            redshift_schema="xp_inc",
            redshift_database="dw",
            redshift_write_mode="insert",
        ),
    ),
    Distribution(
        consumers=[
            Consumer(
                type="Datamart",
                consumption_purpose="Exemplo — substituir pelos consumidores reais do Positivador.",
                how="Exemplo — substituir pelos consumidores reais do Positivador.",
                owner=Contact(
                    name="Performance",
                    contact_emails=["performance.best@investsmart.com.br"],
                ),
                delivery_sla=1,
                delivery_deadline="Após inserção, 3h da manhã do dia seguinte",
            ),
        ],
    ),
    Transformation(
        functions=[
            Function(
                name="exemplo",
                description="Exemplo — substituir pelas transformações reais aplicadas ao Positivador.",
            ),
        ],
    ),
    BusinessRules(
        rules=[
            Rule(
                name="exemplo",
                description="Regra de exemplo — substituir pelas regras de negócio reais do Positivador.",
            ),
        ],
    ),
)
