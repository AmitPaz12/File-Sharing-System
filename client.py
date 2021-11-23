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


def push_folder_to_server(sock, folder_path):
    sock.send(b'add my folder')
    # folder_id = s.recv(150)
    push_data(folder_path, sock)


def pull_folder_from_server(sock, my_path, folder_name):
    sock.send(folder_name.encode())
    pull_data(my_path, sock)


if __name__ == '__main__':
    ip_server = sys.argv[1]
    port_server = int(sys.argv[2])
    path = sys.argv[3]
    timer = int(sys.argv[4])
    s = connect_to_server(ip_server, port_server)
    if len(sys.argv) == 6:
        folder_id = sys.argv[5]
        pull_folder_from_server(s, path, folder_id)

    else:
        client_id = None
        push_folder_to_server(s, path)

    s.close()

    # watchdog
    while True:
        print('fuck hemi')