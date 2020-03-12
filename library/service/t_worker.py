from library.base.process import process_path
import traceback
import json
import time


class RpcParamsException(Exception):
    pass


class Worker(object):
    def __init__(self, logger):
        self._logger = logger

    def call(self, body):
        start = time.time()
        try:
            response = self._process(body)
            self._logger.info("incoming:{} {}s".format(body, round(time.time() - start, 3)))

            status = response.get("status", 0) if type(response) == dict else 0
            msg = str(response.get("msg", "")) if type(response) == dict else ""

            if status != 0:
                response = self._get_error(msg)
            else:
                result = response
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
    def _process(cls, body):
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

        if path is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少path"))

        if params is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少params"))

        try:
            result = process_path(path, params)
        except ModuleNotFoundError:
            raise RpcParamsException("参数错误:{}:{}".format(body, "path 不存在"))

        return result
