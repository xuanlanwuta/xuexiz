from socket import *
import multiprocessing
class Tcp_socket(object):
    def __init__(self):
        self.tcp_sock = socket(AF_INET, SOCK_STREAM)
        self.tcp_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcp_sock.bind(("", 8888))
        self.tcp_sock.listen(128)

    def run(self):
        while True:
            ke_sock, ke_ip = self.tcp_sock.accept()
            a = multiprocessing.Process(target=self.ke_jie, args=(ke_sock,))
            a.start()

    def ke_jie(self, ke_sock):
        ret = ke_sock.recv(1024).decode()
        if not ret:
            return
        else:
            ke_sock.send(ret.encode())


def main():
    a= Tcp_socket()
    a.run()


if __name__ == '__main__':
    main()
