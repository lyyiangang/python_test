import socket
import time

class ClientWrapper:
    def __init__(self, ip : str, port : int):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        self.cb_fun = None
    
    def run(self):
        while True:
            data = self.s.recv(1024).decode('utf-8')
            if self.cb_fun is not None:
                self.cb_fun(data)

if __name__ == '__main__':
    c = ClientWrapper('127.0.0.1', 9999)
    c.cb_fun = lambda xx : print(xx)
    c.run()