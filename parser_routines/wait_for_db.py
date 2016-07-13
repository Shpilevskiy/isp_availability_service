import sys
import time
import logging

import psycopg2

NUMBER_OF_ATTEMPTS = 5
INITIAL_SLEEP_DELAY = 1

# Number of seconds added to previous delay
DELAY_INCREMENT = 2

attempts_made = 0
current_delay = INITIAL_SLEEP_DELAY

while attempts_made < NUMBER_OF_ATTEMPTS:
    try:
        # TODO: read credentials from environment variables
        psycopg2.connect(host="db",
                         database="postgres",
                         user="postgres")
        logging.warn("Connection succeeded.")
        sys.exit(0)
    except Exception as e:
        msg = "Connection DID NOT succeed, waiting for {} seconds: {}."
        logging.warn(msg.format(current_delay, str(e)))
        time.sleep(current_delay)
        current_delay += DELAY_INCREMENT
        attempts_made += 1

logging.warn("Could not connect to the database.")
sys.exit(1)
