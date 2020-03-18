from library.service.t_logger import Logger
from library.base.controller import BaseController
from library.base.get_param import check_params
from models.hello.hello_world import HelloWorld
import flask_admin as admin


class Hello(BaseController):                              # controller 不能重名

    @admin.expose("/echo", methods=["POST", "GET"])       # thrift 请求使用 post 方式注入, 此处必须有 POST
    @check_params
    def echo(self):
        content = self.params["content"]
        name = self.params["name"]                        # 获取参数

        logger = Logger.get_instance().get_module_logger()
        logger.debug("into echo content")

        result = HelloWorld.get_instance(logger=logger).echo("{}, {}".format(content, name))

        return self.show_result(result)                   # 包装返回
