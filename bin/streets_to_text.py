"""
This script helps to write all connections'
streets into the text file
"""

import os
import sys
import argparse
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, "..", "parser_routines"))

from by_isp_coverage.utils import get_parser_class_by_name, get_parsers
from by_isp_coverage.validators import ConnectionValidator


logger = logging.getLogger('utils.fill_db')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parsers',
                        nargs='+', help='Parser names to be used')
    parser.add_argument('-o', '--output-file',
                        default="streets-output.txt",
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
    street_set = set()
    for parser_class in parsers:
        logger.info("Parsing data from {} ISP".format(parser_class.PARSER_NAME))
        p = parser_class(None, validator=ConnectionValidator())
        connections = p.get_connections()
        for c in connections:
            street_set.add(c.street)

    with open(args.output_file, "w", encoding="utf-8") as f:
        for s in sorted(street_set):
            f.write(s + "\n")

if __name__ == '__main__':
    main()
