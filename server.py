from library.protocol.thrift import ThriftService
from library.service import worker, t_server, logger
from config.settings import PROJECT_NAME, LOG_PATH

if __name__ == '__main__':
    handler = worker.Worker(logger.get_global_logger(PROJECT_NAME, LOG_PATH))
    server = t_server.ThriftServer("0.0.0.0", 9090, handler, ThriftService, 4)
    server.start()
