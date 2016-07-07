import json

import falcon
from sqlalchemy import create_engine
from sqlalchemy.sql import text


class HelloWorldResource(object):
    def on_get(self, req, resp):
        data = {"text": "Hello, world and you also!"}
        resp.body = json.dumps(data)

class CitiesResource(object):
    def on_get(self, req, resp):
        # Only for local development
        # After nginx will be set up CORS policy should work properly
        # and headers below must be removed
        resp.set_headers({"Access-Control-Allow-Origin": "*"})
        query = req.get_param('q', default="")

        engine = create_engine('postgresql+psycopg2://postgres:@db/postgres',
                               isolation_level="READ UNCOMMITTED", echo=True)

        if not query:
            resp.body = json.dumps({"cities": []})
        else:
            with engine.connect() as con:
                statement = text("""
                                SELECT "City".city_name AS "City_city_name"
                                FROM "City"
                                WHERE "City".city_name LIKE :name
                                """)
                result = con.execute(statement, name=query.lower() + '%')
                response = [r[0] for r in result]
            json_responce = {"cities": response}
            print(json_responce)
            resp.body = json.dumps(json_responce)
            resp.status = falcon.HTTP_200

api = falcon.API()
api.add_route('/hello', HelloWorldResource())
api.add_route('/cities', CitiesResource())
