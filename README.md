# rpc-service

*python thrift rpc service*

## 运行环境

> Python 3.6


## 目录结构

```
├── config   // 配置文件
│   ├── production   // 生产环境配置（不加入版本控制）
│   ├── settings.py  // 设置运行环境 dev/product
│   └── params  // 设置参数验证(https://docs.python.org/zh-cn/3/library/argparse.html)
├── files    // 运行时需要的一些文件（不加入版本控制）
├── library  // 本地类库
├── models   // 业务模型
├── modules  // 业务模块
└── requirements.txt  // 项目依赖包
```

## CLI 统一入口

> python3 app.py --uri="/say/hello/echo_content" --content="hello world"

## API

使用 thrift 通信, 使用 flask 作为程序路由

```
path, params = self.check_params(body)

ctx = self.app.test_request_context(
    path=path,
    json=params,
    method="POST",
)

# 开启上下文
ctx.push()

# 注入上下文, 每个请求的环境独立
g.params = params
response = self.app.full_dispatch_request()

# 结束上下文
ctx.pop()

if response.status_code == 200:
    data = response.data
    if isinstance(data, bytes):
        data = data.decode()

    resp = json.loads(data)
```

## MODULES

### 创建 controller

*程序 modules 目录下*


```
# modules/say/controllers/hello.py

from library.base.controller import BaseController        # 引入 BaseController
import flask_admin as admin


class Hello(BaseController):                              # controller 不能重名
    @admin.expose("/echo", methods=["POST", "GET"])       # thrift 请求使用 post 方式注入, 此处必须有 POST
    def echo(self):
        content = self.params["content"]
        name = self.params["name"]                        # 获取参数

        logger = Logger.get_instance().get_module_logger()
        logger.debug("into echo content")

        result = HelloWorld.get_instance(logger=logger).echo("{}, {}".format(content, name))

        return self.show_result(result)                   # 包装返回
```


### 参数校验

#### 创建 params 文件

```
# 创建config/params/{module}/{controller}.py

param_check = {
    "echo": {
        "content": {"type": str, "required": True},
        "name": {"type": str, "required": False, "default": "Stranger"}
    }
}

```

#### controller 加入 修饰器

```
# modules/say/controllers/hello.py

from library.base.controller import BaseController        # 引入BaseController
from library.base.get_param import check_params
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
```

#### controller 注入 flask

```
# library/base/flask_admin.py

from flask_admin import Admin
from modules.say.controllers.hello import Hello


admin = Admin(name="admin")
admin.add_view(Hello(name="say.hello", url="/say/hello"))

```