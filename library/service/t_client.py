from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
import logging


class ThriftClient:
    def __init__(self, ip, port, module_file, timeout_ms=3 * 1000):
        self._ip = ip
        self._port = port
        self._module_file = module_file
        self._timeout_ms = timeout_ms

        self._socket_obj = TSocket.TSocket(host=self._ip, port=self._port)
        self._socket_obj.setTimeout(self._timeout_ms)
        self._transport = TTransport.TBufferedTransport(self._socket_obj)
        self._protocol = TBinaryProtocol.TBinaryProtocol(self._transport)

        self._client = self._module_file.Client(self._protocol)

    def __enter__(self):
        if not self._transport.isOpen():
            try:
                self._transport.open()
            except Thrift.TException as e:
                logging.error("ERROR")
                raise Exception(str(e))

            logging.info("ERROR")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._transport.isOpen():
            self._transport.close()
            logging.info("connection closed")

    def request(self, method_name_str, *args):
        try:
            result = getattr(self._client, method_name_str)(*args)
        except Exception as e:
            logging.error("ERROR. %s" % [method_name_str, args])

            if self._transport.isOpen():
                self._transport.close()
                logging.warning("request:: is closed")

            raise Exception(str(e))
        else:
            return result
