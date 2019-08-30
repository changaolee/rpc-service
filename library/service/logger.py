import logging
import os


def get_logger(log_name: str, path: str):
    log_format = "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt="%Y-%m-%d %H:%M:%S", handlers=[
        logging.FileHandler(
            filename="{0}/{1}.log".format(path, log_name),
            encoding="utf8"
        ),
        logging.StreamHandler()
    ])
    logger = logging.getLogger(log_name)
    return logger


def get_global_logger(project_name, log_path):
    path = "{}{}".format(log_path, project_name)
    if not os.path.exists(path):
        os.makedirs(path)

    return get_logger(project_name, path)
