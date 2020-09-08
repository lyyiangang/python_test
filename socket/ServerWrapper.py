import socket
import threading
import time
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
    # s = ServerWarpper('127.0.0.1', 9999) # for local machine
    s = ServerWarpper('0.0.0.0', 9999) # for LAN clinet
    for cmd in 'abcd':
        s.send_command(cmd)
        time.sleep(0.01)