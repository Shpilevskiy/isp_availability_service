from db import engine, session
from models import Base, ISP

from sqlalchemy import exists

from by_isp_coverage.utils import get_parsers


def create_isp_tables():
    parser_classes = get_parsers()
    for cls in parser_classes:
        if not session.query(exists().where(ISP.name == cls.PARSER_NAME)).scalar():
            session.add(ISP(name=cls.PARSER_NAME, url=cls.PARSER_URL))
            session.commit()


def main():
    Base.metadata.create_all(engine)
    create_isp_tables()

if __name__ == '__main__':
    main()
