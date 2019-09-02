from library.protocol.thrift import ThriftService
from library.service import t_worker, t_server
from library.service.t_logger import Logger

if __name__ == '__main__':
    handler = t_worker.Worker(Logger.get_instance().get_global_logger())
    server = t_server.ThriftServer("0.0.0.0", 9090, handler, ThriftService, 4)
    server.start()
