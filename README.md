# data-contracts

Repositório central de **contratos de dados** (data contracts) da InvestSmart. Cada dataset ingerido/distribuído pela engenharia de dados é descrito por um `DataContract`: um objeto Python que documenta origem, extração, schema, qualidade, ingestão, distribuição, transformações e regras de negócio de um dado — tudo em um único lugar, versionado junto com o código.


## Instalação

O projeto usa [uv](https://docs.astral.sh/uv/) para gerenciamento de dependências e ambiente (Python >= 3.12).

```bash
uv sync
```

## Como criar um novo contrato

1. Crie um arquivo em `data_contracts/definitions/<parceiro_ou_fonte>/<dataset>.py`.
2. Use [data_contracts/model/example.py](data_contracts/model/example.py) como ponto de partida — ele mostra o preenchimento de cada bloco (`General`, `DataSource`, `DataExtraction`, `DataSchema`, `DataQuality`, `DataIngestion`, `Distribution`, `Transformation`, `BusinessRules`) com comentários explicando o propósito de cada campo.
3. Declare o schema do dataset como um `BaseModel` do Pydantic (`DataSchema(model=...)`), marcando colunas especiais via `Field(json_schema_extra=...)`:
   - `unique_key: True` — coluna(s) que formam a chave de negócio do dataset. O `DataContract` sincroniza automaticamente o check `check_no_duplicates` em `DataQuality` a partir dessas colunas — não declare esse check manualmente.
   - `sensitive: True` — coluna contém dado pessoal/PII sujeito à LGPD (CPF, e-mail, nome, etc.), independente de ser ou não chave.
4. Exporte o `DataContract` resultante em [data_contracts/definitions/registry.py](data_contracts/definitions/registry.py).
