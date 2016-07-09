import logging

from celery import Celery
from by_isp_coverage import ByflyParser

from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker

from engine import engine
from models import ISP, Status, Connection

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)


def fill_db_from_connections(connections):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    for connection in connections:
        if not session.query(exists().where(ISP.name == connection.provider)).scalar():
            session.add(ISP(name=connection.provider, url='test'))
            session.commit()
        isp = session.query(ISP).filter(ISP.name == connection.provider).first()
        if not session.query(exists().where(Status.status == connection.status)).scalar():
            session.add(Status(status=connection.status))
            session.commit()
        status = session.query(Status).filter(Status.status == connection.status).first()
        if not session.query(Connection).filter(Connection.region == connection.region,
                                                Connection.city == connection.city,
                                                Connection.street == connection.street,
                                                Connection.house_number == connection.house).count():

            session.add(Connection(region=connection.region, city=connection.city,
                                   street=connection.street, house_number=connection.house,
                                   isp=isp, status=status))
            session.commit()
        # need to check connection status for changes


@celery.task
def load_byfly_data():
    parser = ByflyParser()
    fill_db_from_connections(parser.get_connections())
