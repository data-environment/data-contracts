from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class DataSchema:
    model: type[BaseModel]

    model_config = {"arbitrary_types_allowed": True}

    def unique_key_columns(self) -> list[str]:
        """Colunas que, juntas, identificam um registro de forma única.

        Uma coluna entra nessa lista quando declarada com
        `Field(json_schema_extra={"unique_key": True})`. Não é
        necessariamente a mesma coisa que a PRIMARY KEY física da tabela de
        destino — por exemplo, em `avenue_fx` o Redshift usa um `id`
        surrogate (auto-increment) como PK física, mas `fx_id` é a chave
        que identifica a operação de verdade na fonte (Avenue). Este método
        é sobre a segunda coisa: a chave de negócio usada para checar
        duplicidade, não a PK técnica do banco de destino.

        Chaves compostas são suportadas por construção: basta marcar todas
        as colunas que, juntas, formam a chave — o método retorna todas as
        colunas flagueadas, sem assumir que existe só uma.

        Usado por `DataContract` para sincronizar automaticamente essa
        chave com o check `check_no_duplicates` de `DataQuality`,
        evitando que as duas fontes de verdade divirjam silenciosamente.
        """
        return self._columns_flagged_as("unique_key")

    def sensitive_columns(self) -> list[str]:
        """Colunas marcadas como dado sensível/PII no schema Pydantic.

        Uma coluna é considerada sensível quando declarada com
        `Field(json_schema_extra={"sensitive": True})` — ex.: CPF, e-mail,
        nome de pessoa física. A sensibilidade é uma característica da
        coluna, não do dataset inteiro: uma tabela pode ter 10 colunas e
        só 2 serem PII. Usar por coluna (em vez de um booleano único no
        schema) é o que permite a uma Op de mascaramento saber exatamente
        o que precisa proteger, em vez de mascarar a tabela inteira ou
        nada.
        """
        return self._columns_flagged_as("sensitive")

    @property
    def has_sensitive_data(self) -> bool:
        """Atalho: True se qualquer coluna do schema for marcada como sensível."""
        return len(self.sensitive_columns()) > 0

    def _columns_flagged_as(self, flag: str) -> list[str]:
        flagged: list[str] = []
        for field_name, field_info in self.model.model_fields.items():
            extra = getattr(field_info, "json_schema_extra", None)
            if isinstance(extra, dict) and extra.get(flag):
                flagged.append(field_name)
        return flagged
