class HelloWorld(object):
    _instance = None
    _logger = None

    @classmethod
    def get_instance(cls, logger=None):
        if logger:
            cls._logger = logger
        if not cls._instance:
            cls._instance = HelloWorld()
        return cls._instance

    def __init__(self):
        pass

    @classmethod
    def echo(cls, content: str):
        cls._logger.info("into hello_world:echo")
        return "echo: " + content
