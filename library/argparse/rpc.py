from library.argparse import argparse
import importlib
import json


def argparse_rpc(uri, params) -> list:
    parser = argparse.ArgumentParser(prefix_chars="")

    try:
        # 获取uri
        uri_list = uri.strip("/").split("/")

        if len(uri_list) != 3:
            raise Exception("request uri error")

        module, controller, method = uri_list
    except Exception as e:
        print("analysis request uri error: uri={}".format(uri))
        raise ModuleNotFoundError("config params {} not found".format(uri))

    try:
        # 验证参数
        params_path = "config.params.{}.{}".format(module, controller)
        params_file = importlib.import_module(params_path)
        params_info = getattr(params_file, "param_check")[method]
        for field, param in params_info.items():
            parser.add_argument(field, **param)

        args = []
        for k, val in params.items():
            if isinstance(val, list):
                val = json.dumps(val)

            args.append("{}={}".format(k, val))

        args = parser.parse_args(args)
    except Exception as e:
        print("check params error:")
        raise e

    args = vars(args)

    return uri, args
