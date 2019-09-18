from config.settings import PROJECT_NAME, LOG_PATH
import traceback
import logging
import time
import os


class Logger(object):
    _project_name = None
    _log_path = None
    _instance = None

    _log_format = "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s"
    _date_format = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Logger()
        return cls._instance

    def __init__(self):
        self._project_name = PROJECT_NAME
        self._log_path = LOG_PATH
        logging.basicConfig(level=logging.DEBUG, format=self._log_format, datefmt=self._date_format)

    def get_global_logger(self):
        path = "{}{}".format(self._log_path, time.strftime("%Y-%m-%d", time.localtime()))
        if not os.path.exists(path):
            os.makedirs(path)

        return self._get_logger(self._project_name, path)

    def get_module_logger(self):
        s = traceback.extract_stack()
        file_path, function = s[-2][0], s[-2][2]
        path = "{}{}{}".format(self._log_path, self._get_module_log_path(file_path), function)
        if not os.path.exists(path):
            os.makedirs(path)

        return self._get_logger(function, path)

    @classmethod
    def _get_module_log_path(cls, file_path):
        path = file_path.split("/")
        return "{}/{}/{}/".format(time.strftime("%Y-%m-%d", time.localtime()), path[-3], path[-1][:-3])

    @classmethod
    def _get_logger(cls, log_name: str, path: str):
        if log_name in logging.root.manager.loggerDict:
            return logging.getLogger(log_name)

        logger = logging.getLogger(log_name)
        fh = logging.FileHandler(
            filename="{}/{}.log".format(path, log_name),
            encoding="utf8"
        )
        ch = logging.StreamHandler()
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
