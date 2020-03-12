from library.service.t_logger import Logger
from library.base.controller import BaseController
from models.hello.hello_world import HelloWorld


class Hello(BaseController):

    def echo_content(self):
        content = self.params["content"]
        name = self.params["name"]

        logger = Logger.get_instance().get_module_logger()
        logger.debug("into echo content")

        result = HelloWorld.get_instance(logger=logger).echo("{}, {}".format(content, name))

        return result
