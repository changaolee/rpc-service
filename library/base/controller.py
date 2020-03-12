class BaseController(object):
    def __init__(self):
        self.params = []

    def set_params(self, params):
        self.params = params
