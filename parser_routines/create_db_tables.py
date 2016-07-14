import logging

from db import engine, session
from models import Base, ISP

from sqlalchemy import exists

from by_isp_coverage.utils import get_parsers

logger = logging.getLogger('parser_routines.create_db_tables')


def fill_provider_data(session):
    """
    We make sure that provider's data is present in
    the database before actually running tasks
    to avoid provider checks on every connection addition.
    """
    logger.warn("Updating provider data.")
    parser_classes = get_parsers()
    for cls in parser_classes:
        if not session.query(exists().where(ISP.name == cls.PARSER_NAME)).scalar():
            session.add(ISP(name=cls.PARSER_NAME, url=cls.PARSER_URL))
            session.commit()


def create_model_tables(engine):
    """Create all of the tables defined in ORM models."""
    logger.warn("Creating models' tables.")
    Base.metadata.create_all(engine)


def main():
    create_model_tables(engine)
    fill_provider_data(session)

if __name__ == '__main__':
    main()
