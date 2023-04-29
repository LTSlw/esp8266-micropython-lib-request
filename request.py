# version = "v0.1.1"

import socket
import ssl


class Request:
    default_port = {
        "http:": 80,
        "https:": 443
    }

    def __init__(
        self,
        method: str = 'GET',
        url: str = '',
        params: dict = None,
        headers: dict = None,
        data: bytes = None
    ):
        self.method = method
        self.url = url
        self.params = {} if params is None else params
        self.headers = {} if headers is None else headers
        self.data = b'' if data is None else data

        splited = self.url.split('/', 3)
        if len(splited) == 3:
            self.proto, _, self.host = splited
            self.path = ''
        elif len(splited) == 4:
            self.proto, _, self.host, self.path = splited
        else:
            raise TypeError('invalid url')

        if ':' in self.host:
            self.host, self.port = self.host.split(':')
            self.port = int(self.port)
        else:
            self.port = self.default_port[self.proto]

        self.enable_ssl = False
        if self.proto == 'https:':
            self.enable_ssl = True

        self.headers['Host'] = self.host
        if data is not None:
            self.headers['Content-Length'] = str(len(self.data))

    def request(self):
        try:
            addrinfo = socket.getaddrinfo(self.host, self.port)[0]
            s = socket.socket(addrinfo[0], addrinfo[1], addrinfo[2])
            s.connect(addrinfo[-1])
            if self.enable_ssl:
                s = ssl.wrap_socket(s, server_hostname=self.host)

            s.write(self.method.upper() + ' ' + self.path + 'HTTP/1.1\r\n')
            for k, v in self.headers.items():
                s.write(k + ': ' + v + '\r\n')
            s.write('\r\n')

            l = s.readline()[0:-2]
            http_version, status_code, reason_phrase = l.decode().split(' ', 2)
            headers = {}

            while True:
                l = s.readline()
                if not l or l == b'\r\n':
                    break
                k, v = l.decode()[0:-2].split(': ', 1)
                headers[k] = v

            data = s.read()
            return Response(http_version=http_version, status_code=status_code, reason_phrase=reason_phrase, headers=headers, data=data)

        except OSError:
            s.close()
            raise

    def request_src(self):
        try:
            addrinfo = socket.getaddrinfo(self.host, self.port)[0]
            s = socket.socket(addrinfo[0], addrinfo[1], addrinfo[2])
            s.connect(addrinfo[-1])
            if self.enable_ssl:
                s = ssl.wrap_socket(s, server_hostname=self.host)

            s.write(self.method.upper() + ' ' + self.path + 'HTTP/1.1\r\n')
            for k, v in self.headers.items():
                s.write(k + ': ' + v + '\r\n')
            s.write('\r\n')
            return s.read()

        except OSError:
            s.close()
            raise


class Response:
    def __init__(
        self,
        http_version: str,
        status_code: str,
        reason_phrase: str,
        headers: dict = None,
        data: bytes = None
    ):
        self.http_version = http_version
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.headers = {} if headers is None else headers
        self.data = bytes(b'') if data is None else data
