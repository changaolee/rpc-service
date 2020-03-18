from flask import g, request

import importlib
from library.argparse import argparse
import json
import functools
from config.params.common import common_params


def check_params(func):
    # 解决 endpoint 重复问题
    @functools.wraps(func)
    def wrapper(*args, **kw):
        get_params()
        return func(*args, **kw)

    return wrapper


def get_params():
    params = get_flask_request_params()

    try:
        uri_list = request.path.strip("/").split("/")

        if len(uri_list) != 3:
            raise Exception("analysis uri error: {}".format(request.path))
        module, controller, method = uri_list

        parser = argparse.ArgumentParser(prefix_chars="")

        # 公共参数
        for field, param in common_params.items():
            parser.add_argument(field, **param)

        # 验证参数
        params_path = "config.params.{}.{}".format(module, controller)
        params_file = importlib.import_module(params_path)

        try:
            params_info = getattr(params_file, "param_check")[method]
        except Exception:
            raise Exception("get config params error: {}".format(request.path))

        for field, param in params_info.items():
            parser.add_argument(field, **param)

        args = []
        for k, val in params.items():
            if isinstance(val, (list, dict)):
                val = json.dumps(val)

            args.append("{}={}".format(k, val))

        args = parser.parse_args(args)
        # 解析过的参数注入上下文
        g.params = vars(args)
    except Exception as e:
        raise Exception(str(e))


def get_flask_request_params():
    params = {}
    # GET
    for item in request.args.lists():
        # item: (name, [value...]), 数组则为多个
        params[item[0].replace("[]", "")] = item[1][0] if len(item[1]) else item[1]

    # POST
    if request.method == "POST":
        # form 表单
        for item in request.form.lists():
            # item: (name, [value...]), 数组则为多个
            params[item[0].replace("[]", "")] = (
                item[1][0] if len(item[1]) == 1 else item[1]
            )

        json_data = request.get_data()
        if json_data:
            if isinstance(json_data, bytes):
                json_data = json_data.decode("utf-8")
            params.update(json.loads(json_data))

    return params
