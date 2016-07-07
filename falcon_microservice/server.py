import json

import falcon
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import MetaData

class HelloWorldResource(object):
    def on_get(self, req, resp):
        data = {"text": "Hello, world and you also!"}
        resp.body = json.dumps(data)


Base = declarative_base()


class City(Base):
    __tablename__ = 'City'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(30), unique=True, nullable=False, index=True)


class CitiesResource(object):
    def on_get(self, req, resp):
        # Only for local development
        # After nginx will be set up CORS policy should work properly
        # and headers below must be removed
        resp.set_headers({"Access-Control-Allow-Origin": "*"})
        query = req.get_param('q', default="")

        engine = create_engine('postgresql+psycopg2://postgres:@db/postgres',
                               isolation_level="READ UNCOMMITTED", echo=True)
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        metadata = MetaData(engine)
        Base.metadata.create_all(engine)

        if not query:
            resp.body = json.dumps({"cities": []})
        else:
            result = session.query(City).filter(City.city_name.contains(query)).all()
            response = [r.city_name for r in result]
            json_responce = {"cities": response}
            print(json_responce)
            resp.body = json.dumps(json_responce)
            resp.status = falcon.HTTP_200

api = falcon.API()
api.add_route('/hello', HelloWorldResource())
api.add_route('/cities', CitiesResource())
