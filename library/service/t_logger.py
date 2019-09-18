from config.settings import PROJECT_NAME, LOG_PATH
import traceback
import logging
import time
import os


class Logger(object):
    _project_name = None
    _log_path = None
    _instance = None

    LOG_FORMAT = "{'@timestamp':'%(asctime)s', 'log_name': '%(name)s', level': '%(levelname)s', 'msg': '%(message)s'}"
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

    _log_format = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Logger()
        return cls._instance

    def __init__(self):
        self._project_name = PROJECT_NAME
        self._log_path = LOG_PATH

    def get_global_logger(self):
        path = "{}{}".format(self._log_path, time.strftime("%Y-%m-%d", time.localtime()))
        if not os.path.exists(path):
            os.makedirs(path)

        return self._get_logger(self._project_name, path)

    def get_module_logger(self):
        s = traceback.extract_stack()
        file_path, function = s[-2][0], s[-2][2]
        module_log_path = self._get_module_log_path(file_path)
        path = "{}{}{}".format(self._log_path, module_log_path, function)
        if not os.path.exists(path):
            os.makedirs(path)

        log_name = '.'.join(module_log_path.split('/')[1:3] + [function])
        return self._get_logger(log_name, path)

    @classmethod
    def _get_module_log_path(cls, file_path):
        path = file_path.split("/")
        return "{}/{}/{}/".format(time.strftime("%Y-%m-%d", time.localtime()), path[-3], path[-1][:-3])

    @classmethod
    def _get_logger(cls, log_name: str, path: str):
        if log_name in logging.root.manager.loggerDict:
            return logging.getLogger(log_name)

        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(
            filename="{}/{}.log".format(path, log_name),
            encoding="utf8"
        )
        fh.setFormatter(cls._log_format)
        ch = logging.StreamHandler()
        ch.setFormatter(cls._log_format)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
