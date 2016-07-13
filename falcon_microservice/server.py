import json
import logging

import falcon

from sqlalchemy.sql import text

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:@db/postgres',
                       isolation_level="READ UNCOMMITTED", echo=False)


def is_city_present(city_name):
    t = text('''SELECT "connection".city as city
                FROM "connection" WHERE city=:name''')
    with engine.connect() as conn:
        result = conn.execute(t, name=city_name)
        return bool(result.scalar())


class HelloWorldResource(object):
    def on_get(self, req, resp):
        data = {"text": "Hello, world and you also!"}
        resp.body = json.dumps(data)


class CitiesResource(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('city_resource')

    def on_get(self, req, resp):
        # Only for local development
        # After NGINX's correct set up CORS policy should work properly
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
            json_response = {"cities": response}
            resp.body = json.dumps(json_response)
        resp.status = falcon.HTTP_200


class ProvidersResource(object):
    def on_get(self, req, resp):
        # Only for local development
        # After NGINX's correct set up CORS policy should work properly
        # and headers below must be removed
        resp.set_headers({"Access-Control-Allow-Origin": "*"})

        with engine.connect() as con:
            statement = text("""
                            SELECT DISTINCT "provider".name, "provider".url
                            FROM "provider"
                            """)
            result = con.execute(statement)
            providers = [{"name": p[0], "url": p[1]} for p in result]
        json_response = {"providers": providers}
        resp.body = json.dumps(json_response)
        resp.status = falcon.HTTP_200


class StreetsResource(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('street_resource')

    def on_get(self, req, resp):
        # Only for local development
        # After NGINX's correct set up CORS policy should work properly
        # and headers below must be removed
        resp.set_headers({"Access-Control-Allow-Origin": "*"})
        city_query = req.get_param('city')
        street_query = req.get_param('street_query')

        self.logger.warn("city_query: {}, street_query: {}".format(city_query, street_query))

        if not street_query:
            err = {"streets": []}
            resp.body = json.dumps(err)
            resp.status = falcon.HTTP_200
            return

        if not city_query:
            self.logger.warn("Empty city supplied")
            err = {"message": "Empty city supplied"}
            resp.body = json.dumps(err)
            resp.status = falcon.HTTP_200
            return
        city_query = city_query.title()
        if not is_city_present(city_query):
            # TODO: decode unicode entries
            msg = "City {} is not found.".format(city_query)
            self.logger.warn(msg)
            err = {"message": msg}
            resp.body = json.dumps(err)
            resp.status = falcon.HTTP_200
            return
        t = text('''SELECT DISTINCT "connection".street as street
                    FROM "connection"
                    WHERE city=:city_name AND street ILIKE :street_name''')

        streets = []
        with engine.connect() as conn:
            result = conn.execute(t,
                                  city_name=city_query,
                                  street_name="%{}%".format(street_query))
            streets = [r[0] for r in result]

        self.logger.warn("Streets: ".format(streets))
        json_response = {"streets": streets}
        resp.body = json.dumps(json_response)
        resp.status = falcon.HTTP_200

api = falcon.API()
api.add_route('/hello', HelloWorldResource())
api.add_route('/cities', CitiesResource())
api.add_route('/providers', ProvidersResource())
api.add_route('/streets', StreetsResource())
