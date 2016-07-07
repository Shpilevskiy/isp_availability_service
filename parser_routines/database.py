from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

Base = declarative_base()


class City(Base):
    __tablename__ = 'City'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(30), unique=True, nullable=False, index=True)


# for some experiments with DB
def main():
    engine = create_engine('postgresql+psycopg2://postgres:@127.0.0.1:5432/postgres',
                           isolation_level="READ UNCOMMITTED", echo=True)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    metadata = MetaData(engine)
    Base.metadata.create_all(engine)

    data = {"city_name_1": "ми"}
    result = []
    with engine.connect() as con:
        statement = text("""
                        SELECT "City".id AS "City_id", "City".city_name AS "City_city_name"
                        FROM "City"
                        WHERE "City".city_name LIKE :city_name_1
                        """)
        result = con.execute(statement, **data)
        print("!")
        for r in result:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(r.city_name)
    # json_responce = {"cities": result}
    # print(json_responce)


if __name__ == '__main__':
    main()
