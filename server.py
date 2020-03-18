from library.protocol.thrift import ThriftService
from library.service import t_worker, t_server
from library.service.t_logger import Logger
from library.base.flask_admin import admin
from flask import Flask
import os

# flask
flaskenv_app_path = os.path.join(os.path.dirname(__file__), "server.py")
os.environ["FLASK_APP"] = flaskenv_app_path

app = Flask(__name__)

admin.init_app(app)
print(app.url_map)

if __name__ == '__main__':
    handler = t_worker.Worker(Logger.get_instance().get_global_logger())
    handler.init_app(app)
    server = t_server.ThriftServer("0.0.0.0", 9090, handler, ThriftService)
    server.start()
