import os
import json
import logging

import falcon

from sqlalchemy.sql import text

from sqlalchemy import create_engine

DEFAULT_DB_CONNECTOR = 'postgresql+psycopg2'
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', "127.0.0.1")
POSTGRES_DATABASE = os.environ.get('POSTGRES_DB', "postgres")
POSTGRES_USER = os.environ.get('POSTGRES_USER', "postgres")
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', "")
POSTGRES_TABLE = os.environ.get('POSTGRES_TABLE', "postgres")
engine_str = '{connector}://{user}:{password}@{host}/{db}'
engine_str = engine_str.format(connector=DEFAULT_DB_CONNECTOR,
                               user=POSTGRES_USER,
                               password=POSTGRES_PASSWORD,
                               host=POSTGRES_HOST,
                               db=POSTGRES_DATABASE)
engine = create_engine(engine_str,
                       isolation_level="READ UNCOMMITTED", echo=False)


def is_city_present(city_name):
    t = text('''SELECT "connection".city as city
                FROM "connection" WHERE city=:name''')
    with engine.connect() as conn:
        result = conn.execute(t, name=city_name)
        return bool(result.scalar())


def is_street_in_city_present(city, street):
    t = text('''SELECT DISTINCT "connection".street as street
        FROM "connection"
        WHERE city=:city_name AND street ILIKE :street_name''')
    with engine.connect() as conn:
        result = conn.execute(t, city_name=city, street_name='%{}%'.format(street))
        return bool(result.scalar())


def check_city_query(city):
    if not city:
        return 'Empty city supplied'
    return


def check_street_query(street):
    if not street:
        return 'Empty street supplied'
    return


def check_city_present(city):
    if not is_city_present(city):
        return 'City {} is not found.'.format(city)
    return


def check_street_in_city_present(city, street):
    if not is_street_in_city_present(city, street):
        return 'Street {} is not found in City {}.'.format(street, city)
    return


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


class SearchResource(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('search_resource')

    def on_get(self, req, resp):
        resp.set_headers({"Access-Control-Allow-Origin": "*"})
        city = req.get_param('city')
        street = req.get_param('street')

        self.logger.warn("city: {}, street: {}".format(city, street))

        error_list = []
        msgs = [check_city_query(city), check_street_query(street)]
        [error_list.append(msg) for msg in msgs if msg is not None]
        if not error_list:
            msgs.append(check_city_present(city.title()))
            msgs.append(check_street_in_city_present(city.title(), street))
            [error_list.append(msg) for msg in msgs if msg is not None]
        if error_list:
            self.logger.warn(error_list)
            response_msg = {'Errors': error_list}
            resp.body = json.dumps(response_msg)
            resp.status = falcon.HTTP_200
            return

        connection = text('''SELECT *
                    FROM "connection"
                    WHERE city=:city_name AND street ILIKE :street_name
                    ''')

        isp = text(""" SELECT "provider".name, "provider".url
                            FROM "provider"
                            WHERE id=:provider_id
                   """)

        status = text(""" SELECT "status".status as status
                              FROM "status"
                              WHERE id=:status_id
                      """)

        with engine.connect() as conn:
            result = conn.execute(connection,
                                  city_name=city,
                                  street_name="%{}%".format(street))
        search_result = []
        for r in result:
            with engine.connect() as conn:
                connection_provider = conn.execute(isp, provider_id=r[1]).first()
                connection_status = conn.execute(status, status_id=r[2])
                search_result.append(
                    {"house": r[6],
                     "provider": connection_provider[0],
                     "provider_url": connection_provider[1],
                     "status": connection_status.first()[0]}
                )

        json_response = {"city": city,
                         "street": street,
                         "connections": search_result}
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
        street_query = req.get_param('street')

        self.logger.debug("city_query: {}, street_query: {}".format(city_query, street_query))

        if not street_query:
            self.logger.debug("Empty street query supplied.")
            err = {"streets": []}
            resp.body = json.dumps(err)
            resp.status = falcon.HTTP_200
            return

        if not city_query:
            self.logger.debug("Empty city query supplied")
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
        self.logger.debug("Streets: {}".format(streets))
        response = {'city': city_query,
                    'items_count': len(streets),
                    'streets': streets}
        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200


api = falcon.API()
api.add_route('/hello', HelloWorldResource())
api.add_route('/cities', CitiesResource())
api.add_route('/providers', ProvidersResource())
api.add_route('/streets', StreetsResource())
api.add_route('/search', SearchResource())