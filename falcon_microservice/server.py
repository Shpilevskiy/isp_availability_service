import json

import falcon


class HelloWorldResource(object):
    def on_get(self, req, resp):
        data = {"text": "Hello, world and you also!"}
        resp.body = json.dumps(data)


cities = {'Минск', 'Гомель', 'Могилев', 'Витебск', 'Гродно', 'Брест',
          'Бобруйск', 'Барановичи', 'Борисов', 'Пинск', 'Орша',
          'Мозырь', 'Солигорск', 'Новополоцк', 'Лида', 'Молодечно',
          'Полоцк', 'Жлобин', 'Светлогорск', 'Речица'}


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
            result = []
            for c in cities:
                if query.lower() in c.lower():
                    result.append(c)
            json_responce = {"cities": result}
            resp.body = json.dumps(json_responce)
            resp.status = falcon.HTTP_200

api = falcon.API()
api.add_route('/hello', HelloWorldResource())
api.add_route('/cities', CitiesResource())
