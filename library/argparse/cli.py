from library.argparse import argparse
import importlib


def argparse_cli(request_uri=["--uri", "-u"]) -> list:
    parser = argparse.ArgumentParser()

    try:
        # 获取uri
        parser.add_argument("--uri", "-u", required=True, help="request uri", type=str)
        args = parser.parse_known_args()[0]
        uri = args.uri
        uri_list = uri.strip("/").split("/")

        if len(uri_list) != 3:
            raise Exception("request uri error")

        module, controller, method = uri_list
    except Exception as e:
        print("analysis request uri error: uri={}".format(uri))
        exit()

    try:
        # 验证参数
        params_path = "config.params.{}.{}".format(module, controller)
        params_file = importlib.import_module(params_path)
        params_info = getattr(params_file, "param_check")[method]
        for field, param in params_info.items():
            field = "--" + field
            parser.add_argument(field, **param)

        args = parser.parse_args()
    except Exception as e:
        print("check params error:")
        exit()

    args = vars(args)
    del args["uri"]

    return uri, args
