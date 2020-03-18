import os
import json
from flask import Flask, g
from library.base.flask_admin import admin

from library.argparse.cli import argparse_cli

# flask
flaskenv_app_path = os.path.join(os.path.dirname(__file__), "server.py")
os.environ["FLASK_APP"] = flaskenv_app_path

app = Flask(__name__)

admin.init_app(app)

uri, params = argparse_cli()

ctx = app.test_request_context(
    path=uri,
    json=params,
    method="POST",
)
ctx.push()

g.params = params
response = app.full_dispatch_request()

ctx.pop()

print(response.status_code)

data = response.data
if isinstance(data, bytes):
    data = data.decode()

if response.status_code == 200:
    data = json.loads(data)
print(data)
