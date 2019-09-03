from library.service.t_logger import Logger
from models.hello.hello_world import HelloWorld


def echo_content(**params):
    content = params.get("content")
    name = params.get("name")

    logger = Logger.get_instance().get_module_logger()
    logger.debug("into echo content")

    result = HelloWorld.get_instance(logger=logger).echo("{}, {}".format(content, name))

    return result
