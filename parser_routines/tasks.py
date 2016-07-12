import logging

from celery import Celery
from by_isp_coverage import ByflyParser, FlynetParser, MTS_Parser, UNETParser, AtlantParser
from by_isp_coverage.validators import ConnectionValidator

from sqlalchemy import exists

from db import session
from models import ISP, Status, Connection
from exceptions import WrongProvider

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)


class SqlAclhemyTask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
        database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        session.remove()


def fill_db_from_connections(connections):
    for connection in connections:
        isp = session.query(ISP).filter(ISP.name == connection.provider).first()
        if not isp:
            raise WrongProvider('No such provider: {}'.format(connection.provider))
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
        else:
            exist_connection = session.query(Connection).filter(Connection.region == connection.region,
                                                                Connection.city == connection.city,
                                                                Connection.street == connection.street,
                                                                Connection.house_number == connection.house).first()
            if exist_connection.status != status:
                exist_connection.status = status
                session.commit()


def call_db_filling(connections):
    try:
        fill_db_from_connections(connections)
    except WrongProvider as error:
        print(error)


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_byfly_data():
    parser = ByflyParser(validator=ConnectionValidator())
    call_db_filling(parser.get_connections())


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_flynet_data():
    parser = FlynetParser(None, validator=ConnectionValidator())
    call_db_filling(parser.get_connections())


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_mts_data():
    parser = MTS_Parser(None, validator=ConnectionValidator())
    call_db_filling(parser.get_connections())


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_unet_data():
    parser = UNETParser(None, validator=ConnectionValidator())
    call_db_filling(parser.get_connections())


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_atlant_data():
    parser = AtlantParser(None, validator=ConnectionValidator())
    call_db_filling(parser.get_connections())
