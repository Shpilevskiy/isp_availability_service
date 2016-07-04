FROM python:3.5

ADD requirements.txt /api/requirements.txt
WORKDIR /api/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' apiuser
CMD su -m apiuser -c "gunicorn -w 2 -b :8000 server:api"
