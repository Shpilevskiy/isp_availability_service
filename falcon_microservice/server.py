import json

import falcon

from sqlalchemy.sql import text

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:@db/postgres',
                       isolation_level="READ UNCOMMITTED", echo=False)


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

        if not query:
            resp.body = json.dumps({"cities": []})
        else:
            with engine.connect() as con:
                statement = text("""
                                SELECT DISTINCT "connection".city AS "connection_city"
                                FROM "connection"
                                WHERE "connection".city ILIKE :name
                                """)
                result = con.execute(statement, name="%{}%".format(query))
                response = [r[0] for r in result]
            json_responce = {"cities": response}
            resp.body = json.dumps(json_responce)
        resp.status = falcon.HTTP_200


class ProvidersResource(object):
    def on_get(self, req, resp):
        # Only for local development
        # After nginx will be set up CORS policy should work properly
        # and headers below must be removed
        resp.set_headers({"Access-Control-Allow-Origin": "*"})

        with engine.connect() as con:
            statement = text("""
                            SELECT DISTINCT "provider".name, "provider".url
                            FROM "provider"
                            """)
            result = con.execute(statement)
            providers = [{"name": p[0], "url": p[1]} for p in result]
        json_responce = {"providers": providers}
        resp.body = json.dumps(json_responce)
        resp.status = falcon.HTTP_200

api = falcon.API()
api.add_route('/hello', HelloWorldResource())
api.add_route('/cities', CitiesResource())
api.add_route('/providers', ProvidersResource())
