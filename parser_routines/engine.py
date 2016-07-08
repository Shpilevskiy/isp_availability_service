from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:@db/postgres',
                       isolation_level="READ UNCOMMITTED", echo=True)
