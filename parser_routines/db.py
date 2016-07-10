from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:@db/postgres',
                       isolation_level="READ UNCOMMITTED", echo=False)

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
