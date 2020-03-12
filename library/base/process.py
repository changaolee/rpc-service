import importlib
from library.argparse.rpc import argparse_rpc


def process_path(uri, params, check_params=True):
    if check_params:
        uri, params = argparse_rpc(uri, params)

    module, controller, method = uri.strip("/").split("/")

    try:
        # 路由module
        controller_path = "modules.{}.controllers.{}".format(module, controller)
        controller_file = importlib.import_module(controller_path)

        # 路由controller
        # 转驼峰
        controller = "".join(map(lambda x: x.capitalize(), controller.split("_")))
        instance = getattr(controller_file, controller)()
        # 注入参数
        instance.set_params(params)

        # 执行method
        func = getattr(instance, method)
    except Exception as e:
        print("uri {} not found:".format(uri))
        raise ModuleNotFoundError("{} not found".format(uri))

    return func()
