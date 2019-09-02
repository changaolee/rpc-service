from config.settings import PROJECT_NAME, LOG_PATH
import logging
import os


class Logger(object):
    _project_name = None
    _log_path = None
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Logger()
        return cls._instance

    def __init__(self):
        self._project_name = PROJECT_NAME
        self._log_path = LOG_PATH

    def get_global_logger(self):
        path = "{}{}".format(self._log_path, self._project_name)
        if not os.path.exists(path):
            os.makedirs(path)

        return self._get_logger(self._project_name, path)

    def get_module_logger(self, file_path, controller):
        path = "{}{}{}".format(self._log_path, self._get_module_log_path(file_path), controller)
        if not os.path.exists(path):
            os.makedirs(path)

        return self._get_logger(controller, path)

    @classmethod
    def _get_module_log_path(cls, file_path):
        path = file_path.split("/")
        return "{}/{}/".format(path[-3], path[-1][:-3])

    @classmethod
    def _get_logger(cls, log_name: str, path: str):
        log_format = "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt="%Y-%m-%d %H:%M:%S", handlers=[
            logging.FileHandler(
                filename="{}/{}.log".format(path, log_name),
                encoding="utf8"
            ),
            logging.StreamHandler()
        ])
        logger = logging.getLogger(log_name)
        return logger
