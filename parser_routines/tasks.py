import logging

from celery import Celery
from by_isp_coverage import ByflyParser

from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker

from engine import engine
from models import City

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)


@celery.task
def load_byfly_data():
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    parser = ByflyParser()
    for c in parser.get_connections():
        if not session.query(exists().where(City.city_name == c.city.lower())).scalar():
            session.add(City(city_name=c.city.lower()))
            session.commit()
