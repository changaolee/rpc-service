class HelloWorld(object):
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = HelloWorld()
        return cls._instance

    def __init__(self):
        pass

    @classmethod
    def echo(cls, content: str):
        return "echo: " + content
