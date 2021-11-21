import os
import random
import socket
import string
import sys
from basic import push_data, pull_data

max_port = 65535
min_port = 1023


def init_clients_folder():
    os.mkdir(os.path.abspath('Clients'))
    return os.path.abspath('Clients')


def create_new_client_id():
    client_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))
    os.mkdir(os.path.join(os.path.abspath('Clients'), client_id))
    return client_id


def create_socket(folder_path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen()

    while True:
        client_socket, client_address = s.accept()
        data = client_socket.recv(150)
        if data.decode() == 'add my folder':
            client_id = create_new_client_id()
            client_socket.send(client_id.encode())
            pull_data(folder_path, s)

        client_socket.close()


# check if port is valid
def check_port(port):
    if not min_port <= port <= max_port:
        sys.exit()


# main method
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    try:
        PORT = int(sys.argv[1])
        check_port(PORT)
        path = init_clients_folder()
        create_socket(path)
    except ValueError:
        sys.exit()
