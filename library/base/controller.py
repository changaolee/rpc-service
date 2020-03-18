import flask_admin as admin
from flask import g, jsonify


class BaseController(admin.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @admin.expose("/")
    def index(self):
        return "xxx"

    @property
    def params(self):
        return getattr(g, "params", {})

    @params.getter
    def get_params(self):
        return getattr(g, "params", {})

    def show_result(self, data):
        return jsonify(data)
