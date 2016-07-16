"""
Purpose of this script is to waith for the container
with the database to be started before actually running parsing
tasks
"""

import sys
import time
import logging

import psycopg2

from .db import POSTGRES_HOST, POSTGRES_DATABASE, POSTGRES_USER

NUMBER_OF_ATTEMPTS = 5
INITIAL_SLEEP_DELAY = 1

# Number of seconds added to previous delay
DELAY_INCREMENT = 2

attempts_made = 0
current_delay = INITIAL_SLEEP_DELAY

logger = logging.getLogger("parser_routines.wait_for_db")

while attempts_made < NUMBER_OF_ATTEMPTS:
    try:
        psycopg2.connect(POSTGRES_HOST,
                         POSTGRES_DATABASE,
                         POSTGRES_USER)
        logger.warn("Connection succeeded.")
        sys.exit(0)
    except Exception as e:
        msg = "Connection DID NOT succeed, waiting for {} seconds: {}."
        logger.warn(msg.format(current_delay, str(e)))
        time.sleep(current_delay)
        current_delay += DELAY_INCREMENT
        attempts_made += 1

logger.warn("Could not connect to the database.")
sys.exit(1)
