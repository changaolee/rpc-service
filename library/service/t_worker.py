from flask import Flask, g
from .t_routes import route_map
import traceback
import json
import time


class RpcParamsException(Exception):
    pass


class Worker(object):
    def __init__(self, logger, app=None):
        self._logger = logger
        self._app = app

    def init_app(self, app: Flask):
        self._app = app

    def call(self, body):
        start = time.time()
        try:
            resp = {}
            if self._app:
                path, params = self._check_params(body)

                ctx = self._app.test_request_context(
                    path=path,
                    json=params,
                    method="POST",
                )

                # 开启上下文
                ctx.push()

                # 注入上下文, 每个请求的环境独立
                g.params = params
                response = self._app.full_dispatch_request()

                # 结束上下文
                ctx.pop()

                if response.status_code == 200:
                    data = response.data
                    if isinstance(data, bytes):
                        data = data.decode()

                    resp = json.loads(data)

            if not resp:
                resp = self._check_params(body)

            self._logger.info("incoming:{} {}s".format(body, round(time.time() - start, 3)))

            status = resp.get("status", 0) if type(resp) == dict else 0
            msg = str(resp.get("msg", "")) if type(resp) == dict else ""

            if status != 0:
                response = self._get_error(msg)
            else:
                result = resp
                response = {
                    "code": status,
                    "message": msg,
                    "result": result
                }
        except RpcParamsException as ex:
            self._logger.debug("traceback.format_exc():____%s" % (traceback.format_exc()))
            self._logger.error("incoming:{} {}".format(body, ex))
            response = self._get_error(str(ex))
        except Exception as ex:
            self._logger.debug("traceback.format_exc():____%s" % (traceback.format_exc()))
            self._logger.error("incoming:{} {}".format(body, ex))
            response = self._get_error(str(ex))

        return json.dumps(response)

    @classmethod
    def _get_error(cls, error_message="", error_code=40001):
        return {
            "code": error_code,
            "message": error_message,
            "result": {}
        }

    @classmethod
    def _check_params(cls, body):
        try:
            j_body = json.loads(body)
        except json.decoder.JSONDecodeError:
            raise RpcParamsException("参数错误:{}:{}".format(body, "json格式错误"))

        j_auth = j_body.get("auth")
        if j_auth is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少auth信息"))

        j_data = j_body.get("request_data")
        if j_data is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少request_data信息"))

        path = j_data.get("url")
        params = j_data.get("params")

        return path, params

    @classmethod
    def _process(cls, body):
        path, params = Worker._check_params(body)

        if path is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少path"))

        if params is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少params"))

        if path in route_map:
            result = route_map[path](**params)
        else:
            raise RpcParamsException("参数错误:{}:{}".format(body, "path 不存在"))

        return result
