import os
import yaml

import tornado.ioloop
import tornado.web
import motor
import pymongo

from urls import handlers


class Application(tornado.web.Application):
    def __init__(self):
        self.async_db = motor.MotorClient().open_sync().teamwall
        self.sync_db = pymongo.MongoClient().teamwall

        root = os.path.dirname(__file__)

        f = open(os.path.join(root, "config/auth.yaml"))
        self.auth_settings = yaml.safe_load(f)
        f.close()

        settings = dict(
            template_path=os.path.join(root, 'templates'),
            static_path=os.path.join(root, 'static'),
            cookie_secret="4a139c72-c40b-4b67-a2fa-9ed942a3ad7f",
            login_url="/login",
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


application = Application()
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
