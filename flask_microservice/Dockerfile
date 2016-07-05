FROM python:3.5

# Install nodejs and npm
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash - \
    && apt-get install -y nodejs

RUN curl -SLO "http://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" \
    && apt-get install -y nodejs \
    && npm install -g npm \
    && npm cache clear

RUN adduser --disabled-password --gecos '' flaskuser

RUN mkdir -p /static/ && chown -R flaskuser: /static/

ADD requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip install -r requirements.txt

# Install bower and front-end dependencies
RUN npm install -g bower


CMD su -m flaskuser -c "ls -la; pwd; cd /app/front_end && bower install"

CMD su -m flaskuser -c "gunicorn -w 2 -b :7000 views:app"