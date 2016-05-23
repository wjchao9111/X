from X.tools.task import gevent_task
from sms.serv.socketlib import SocketServer, SocketClient


class FORWARD_SERVER:
    def __init__(self, serv_addr, forward_addr):
        self.serv_sock = SocketServer(serv_addr)
        self.forward_addr = forward_addr
        self.start()
        self.session_list = {}

    @gevent_task
    def start(self):
        self.serv_sock.listen(backlog=10)
        while True:
            client_sock = self.serv_sock.accept(frame_handler=None)
            session = FORWARD_SESSION(self)
            session.accept(client_sock)
            self.push_list(session)

    def push_list(self, session):
        self.session_list[session] = None

    def terminate(self, session):
        try:
            self.session_list.pop(session)
        except:
            pass


class FORWARD_SESSION:
    def __init__(self, SERVER):
        self.SERVER = SERVER
        self.client_sock = None
        self.server_sock = None

    @gevent_task
    def accept(self, sock):
        try:
            target = self.SERVER.forward_addr
            self.server_sock = sock
            self.client_sock = SocketClient(None, target, frame_handler=None, name='client')
            self.client_sock.connect()
            self.start_client()
            self.start_server()
        except:
            self.close()

    @gevent_task
    def start_server(self):
        try:
            while True:
                frame = self.server_sock.recv()
                if frame is not None:
                    self.client_sock.send(frame)
                else:
                    break
        except:
            pass
        finally:
            self.close()

    @gevent_task
    def start_client(self):
        try:
            while True:
                frame = self.client_sock.recv()
                if frame is not None:
                    self.server_sock.send(frame)
                else:
                    break
        except:
            pass
        finally:
            self.close()

    def close(self):
        self.idle = True
        if self.server_sock:
            self.server_sock.close()
        if self.client_sock:
            self.client_sock.close()
        self.SERVER.terminate(self)
