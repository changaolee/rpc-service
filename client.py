from library.protocol.thrift import ThriftService
from library.service import t_client
import json

if __name__ == '__main__':
    request_data_list = [
        {
            "url": "/say/hello/echo",
            "params": {
                "content": "Hello world"
            }
        }
    ]
    with t_client.ThriftClient("127.0.0.1", 9090, ThriftService) as client:
        for request_data in request_data_list:
            request_body = {
                "auth": {
                    "app_key": "key",
                    "app_sec": "secret",
                },
                "request_data": request_data
            }
            resp = client.request("call", json.dumps(request_body))
            print(resp)
