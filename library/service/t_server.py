from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.server import TProcessPoolServer
from multiprocessing import cpu_count
import logging


class ThriftServer:
    def __init__(self, ip, port, handler_obj, service_module, num_workers=None):
        self._ip = ip
        self._port = port
        self._handler_obj = handler_obj
        self._service_module = service_module
        self._num_workers = num_workers or cpu_count()

        self._processor = service_module.Processor(self._handler_obj)
        self._server_socket = TSocket.TServerSocket(
            host=self._ip, port=self._port)
        self._transport = TTransport.TBufferedTransportFactory()
        self._protocol = TBinaryProtocol.TBinaryProtocolFactory()

        # 使用进程池方式
        self._server = TProcessPoolServer.TProcessPoolServer(
            self._processor, self._server_socket, self._transport, self._protocol)
        self._server.setPostForkCallback(self.process_callback)
        self._server.setNumWorkers(self._num_workers)

    @staticmethod
    def process_callback():
        logging.info("start new worker")

    def start(self):
        logging.info("start rpc server")
        self._server.serve()
