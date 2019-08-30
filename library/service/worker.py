import time
import json
import traceback
import importlib


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
        except Exception as e:
            self._logger.error("traceback.format_exc():____%s" % (traceback.format_exc()))
            response = self._get_error(str(e))

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
            _, module, controller, method = path.split("/")
            action = importlib.import_module("modules.{}.controllers.{}".format(module, controller))
            func = getattr(action, method)
        except:
            raise RpcParamsException("参数错误:{}:{}".format(body, "路径解析失败"))

        try:
            config_file = importlib.import_module("config.params.{}.{}".format(module, controller))
            param_config_info = getattr(config_file, "param_check")[method]
        except:
            raise RpcParamsException("参数错误:{}:{}".format(body, "未找到参数配置文件"))

        for defined_param, defined_param_info in param_config_info.items():
            if not params.get(defined_param):
                if defined_param_info.get("need_necessary"):
                    raise RpcParamsException("参数错误:{}:{}".format(body, "缺少参数{}".format(defined_param)))
                else:
                    params[defined_param] = defined_param_info["default"]
            else:
                try:
                    params[defined_param] = defined_param_info["type"](params[defined_param])
                except:
                    raise RpcParamsException(
                        "参数错误:{}:{}".format(body, "需要{}类型的参数{}".format(defined_param_info["type"], defined_param)))

        result = func(**params)

        return result
