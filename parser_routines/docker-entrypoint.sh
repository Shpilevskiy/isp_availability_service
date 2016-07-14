#!/bin/bash

dbhost="db"
dbuser="postgres"
dbpassword="postgres"

echo "Checking whether database is available."
(python3 /app/parser_routines/wait_for_db.py)

if [ $? -ne 0 ]; then
    echo "Database connection anavailable"
    exit 1
fi

# Create all initial tables
echo "Initialising database data."
python3 /app/parser_routines/create_db_tables.py

# Launch celery beat and celery workers
supervisord -c /etc/supervisor/conf.d/supervisord.conf