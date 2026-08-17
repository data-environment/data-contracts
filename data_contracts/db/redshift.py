import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

dotenv.load_dotenv()


def get_redshift_engine() -> Engine:
    """Cria a engine SQLAlchemy do Redshift a partir de variáveis de ambiente.

    Requer REDSHIFT_HOST, REDSHIFT_PORT, REDSHIFT_USER e REDSHIFT_PASS.
    REDSHIFT_DATABASE é opcional, com "dw" como padrão.
    """
    host = os.environ["REDSHIFT_HOST"]
    port = os.environ["REDSHIFT_PORT"]
    user = os.environ["REDSHIFT_USER"]
    password = os.environ["REDSHIFT_PASS"]
    database = os.environ.get("REDSHIFT_DATABASE", "dw")
    return create_engine(f"redshift+psycopg2://{user}:{password}@{host}:{port}/{database}")
