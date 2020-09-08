import socket
import threading
import time


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 监听端口:
# s.bind(('127.0.0.1', 9999))
# s.listen(5)
# print('Waiting for connection...')
# while True:
#     # 接受一个新连接:
#     sock, addr = s.accept()
#     # 创建新线程来处理TCP连接:
#     t = threading.Thread(target=tcplink, args = (sock, addr))
#     t.start()

class ServerWarpper:
    def __init__(self, ip : str, port : int, max_connection_num : int = 5):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip, port))
        self.s.listen(5)
        print('sever waiting for connection...')
        self.cmd = None
        self.cmd_lock = threading.Lock()
        host_sock, addr = self.s.accept()
        self.t = threading.Thread(target = self.tcplink, args = (host_sock, addr))
        self.t.start()
        
    def send_command(self, cmd):
        self.cmd_lock.acquire()
        self.cmd = cmd
        self.cmd_lock.release()

    def tcplink(self, sock, addr):
        print('Accept new connection from %s:%s...' % addr)
        while True:
            self.cmd_lock.acquire()
            if self.cmd:
                sock.send(b'%s' % self.cmd.encode('utf-8'))
                self.cmd = None
            self.cmd_lock.release()
            time.sleep(0.001)
        sock.close()
        print('Connection from %s:%s closed.' % addr) 

if __name__ == '__main__':
    s = ServerWarpper('127.0.0.1', 9999)
    for cmd in 'abcd':
        s.send_command(cmd)
        time.sleep(0.01)