from library.service.t_logger import Logger
from models.hello.hello_world import HelloWorld

# logger = Logger.get_instance().get_module_logger("/say/hello")


def echo_content(**params):
    content = params.get("content")
    name = params.get("name")

    result = HelloWorld.get_instance().echo("{}, {}".format(content, name))

    return result
