import logging

from celery import Celery
from by_isp_coverage import (
    AtlantParser,
    ByflyParser,
    FlynetParser,
    MTS_Parser,
    UNETParser,
)
from by_isp_coverage.validators import ConnectionValidator

from db import session
from utils import call_db_filling

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)


class SqlAclhemyTask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
        database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        session.remove()


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_byfly_data():
    parser = ByflyParser(validator=ConnectionValidator())
    call_db_filling(session, parser.get_connections())


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_flynet_data():
    parser = FlynetParser(None, validator=ConnectionValidator())
    call_db_filling(session, parser.get_connections())


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_mts_data():
    parser = MTS_Parser(None, validator=ConnectionValidator())
    call_db_filling(session, parser.get_connections())


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_unet_data():
    parser = UNETParser(None, validator=ConnectionValidator())
    call_db_filling(session, parser.get_connections())


@celery.task(base=SqlAclhemyTask, max_retries=5, default_retry_delay=30)
def load_atlant_data():
    parser = AtlantParser(None, validator=ConnectionValidator())
    call_db_filling(session, parser.get_connections())
