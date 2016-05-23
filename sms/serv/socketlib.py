# import socket
import os

from X.tools.task import socket, ssl


class SocketServer:
    def __init__(self, serv_addr):
        self.serv_addr = serv_addr
        self.sock = None

    def listen(self, backlog):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.serv_addr)
        self.sock.listen(backlog)

    def accept(self, frame_handler):
        conn, accept_addr = self.sock.accept()
        client_sock = SocketClient(
            source=accept_addr,
            target=self.serv_addr,
            frame_handler=frame_handler,
            name='Client_' + str(accept_addr)
        )
        client_sock.sock = conn
        return client_sock


class SSLServer(SocketServer):
    def get_cert(self):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(BASE_DIR, 'serv', 'cert', 'cert.pem')
        return path

    def get_key(self):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(BASE_DIR, 'serv', 'cert', 'key.pem')

    def accept(self, frame_handler):
        conn, accept_addr = self.sock.accept()
        ssl_client = ssl.wrap_socket(conn,
                                     server_side=True,
                                     certfile=self.get_cert(),
                                     keyfile=self.get_key(),
                                     ssl_version=ssl.PROTOCOL_TLSv1)

        client_ssl = SSLClient(
            source=accept_addr,
            target=self.serv_addr,
            frame_handler=frame_handler,
            name='SSLClient_' + str(accept_addr)
        )
        client_ssl.sock = ssl_client
        return client_ssl


class SocketClient:
    def __init__(self, source, target, frame_handler=None, name=None):
        self.name = name
        self.source = source
        self.target = target
        self.frame_size = 1024

        self.frame_handler = frame_handler
        if not isinstance(self.frame_handler, SocketFrameHandler):
            self.frame_handler = SocketFrameHandler()

        self.buffer = ''
        self.sock = None

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.source:
            self.source = (self.source[0], int(self.source[1]))
            sock.bind(self.source)
        self.target = (self.target[0], int(self.target[1]))
        sock.connect(self.target)

        self.sock = sock
        self.buffer = ''

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass

    def raw_recv(self):
        # time.sleep(0.01)
        data = None
        try:
            data = self.sock.recv(self.frame_size)
        except Exception:
            pass
        finally:
            return data

    def recv(self):
        while True:
            frame, self.buffer = self.frame_handler.recv_frame(self.buffer)
            if frame:
                return frame
            else:
                data = self.raw_recv()
                if data:
                    self.buffer += data
                else:
                    return None

    def raw_send(self, data, sock=None):
        if sock is None:
            sock = self.sock
        sock.send(data)

    def send(self, frame, sock=None):
        self.raw_send(self.frame_handler.send_frame(frame), sock)


class SSLClient(SocketClient):
    def get_cert(self):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(BASE_DIR, 'serv', 'cert', 'cert.pem')
        return path

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssl_sock = ssl.wrap_socket(sock,
                                   ca_certs=self.get_cert(),
                                   cert_reqs=ssl.CERT_REQUIRED)
        if self.source:
            self.source = (self.source[0], int(self.source[1]))
            ssl_sock.bind(self.source)
        self.target = (self.target[0], int(self.target[1]))
        ssl_sock.connect(self.target)

        self.sock = ssl_sock
        self.buffer = ''


class SocketFrameHandler:
    def __init__(self):
        pass

    def recv_frame(self, data):
        return data, ''

    def send_frame(self, frame):
        return frame
