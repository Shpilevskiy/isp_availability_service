"""
Entrypoint for all of the modules referring
database connection.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DEFAULT_DB_CONNECTOR = 'postgresql+psycopg2'
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', "127.0.0.1")
POSTGRES_DATABASE = os.environ.get('POSTGRES_DB', "postgres")
POSTGRES_USER = os.environ.get('POSTGRES_USER', "postgres")
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', "")
POSTGRES_TABLE = os.environ.get('POSTGRES_TABLE', "postgres")


engine_str = '{connector}://{user}:{password}@{host}/{db}'
engine_str = engine_str.format(connector=DEFAULT_DB_CONNECTOR,
                               user=POSTGRES_USER,
                               password=POSTGRES_PASSWORD,
                               host=POSTGRES_HOST,
                               db=POSTGRES_DATABASE)
engine = create_engine(engine_str,
                       isolation_level="READ UNCOMMITTED", echo=False)

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
