import tornado.web
from lib import RequestHandler


class Handler(RequestHandler):
    @tornado.web.authenticated
    def get(self):
        params = {}
        self.render("index.html", **params)
