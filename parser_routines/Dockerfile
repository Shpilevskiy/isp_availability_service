FROM python:3.5

ADD requirements.txt /app/parser_routines/requirements.txt
WORKDIR /app/
RUN pip install -r parser_routines/requirements.txt
# This shit fails, WHY??
CMD celery -A parser_routines.tasks worker -l debug --beat