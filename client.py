import os
import socket
import sys
from basic import push_data, pull_data


def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def create_folder():
    os.mkdir(os.path.abspath())


def connect_to_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    return s


def upload_folder_to_server(ip, port, folder_path):
    s = connect_to_server(ip, port)
    s.send(b'add my folder')
    folder_id = s.recv(150)
    push_data(folder_path, s)


if __name__ == '__main__':
    ip_server = sys.argv[1]
    port_server = int(sys.argv[2])
    path = sys.argv[3]
    timer = int(sys.argv[4])
    if len(sys.argv) == 6:
        client_id = sys.argv[5]
        create_folder()
        connect_to_server(ip_server, port_server)
    else:
        client_id = None
        upload_folder_to_server(ip_server, port_server, path)


