import json

import falcon


class HelloWorldResource(object):
    def on_get(self, req, resp):
        data = {"text": "Hello, world and you also!"}
        resp.body = json.dumps(data)


api = falcon.API()
api.add_route('/hello', HelloWorldResource())
