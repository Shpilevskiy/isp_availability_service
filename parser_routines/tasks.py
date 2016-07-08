from celery import Celery
from by_isp_coverage import ByflyParser
from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from database import City, Base

celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def load_byfly_data():
    engine = create_engine('postgresql+psycopg2://postgres:@db/postgres',
                           isolation_level="READ UNCOMMITTED", echo=True)
    metadata = MetaData(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    parser = ByflyParser()
    for c in parser.get_connections():
        if not session.query(exists().where(City.city_name == c.city.lower())).scalar():
            session.add(City(city_name=c.city.lower()))
            session.commit()
