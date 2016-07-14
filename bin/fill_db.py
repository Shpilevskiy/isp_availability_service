"""
This file contains methods to fill DB data without
running celery tasks
"""

import os
import sys
import argparse
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, "..", "parser_routines"))

from by_isp_coverage.utils import get_parser_class_by_name, get_parsers
from by_isp_coverage.validators import ConnectionValidator

from create_db_tables import fill_provider_data, create_model_tables
from db import engine, session
from utils import call_db_filling

logger = logging.getLogger('utils.fill_db')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parsers',
                        nargs='+', help='Parser names to be used')
    parser.add_argument('-d', '--drop-db',
                        action='store_true',
                        help='Drop all existing data.')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.parsers is None:
        parsers = get_parsers()
    else:
        # Try to get parser classes by their names
        # as specified by the user
        parsers = []
        for p_name in args.parsers:
            try:
                parser = get_parser_class_by_name(p_name)
                parsers.append(parser)
            except NameError:
                msg = "Unknown provider {}, skipping..."
                logger.warn(msg.format(p_name))
    if args.drop_db:
        # logger.warn("Dropping all databases.")
        # TODO: add logics to drop all existing tables
        pass

    create_model_tables(engine)
    fill_provider_data(session)

    for parser_class in parsers:
        logger.info("Parsing data from {} ISP".format(parser_class.PARSER_NAME))
        p = parser_class(None, validator=ConnectionValidator())
        connections = p.get_connections()
        call_db_filling(session, connections)
        logger.info("Data succesfully loaded into the database.")

if __name__ == '__main__':
    main()
