import os
import random
import socket
import string
import sys
from basic import push_data, pull_data

max_port = 65535
min_port = 1023

clients_dic = {}


def add_to_dic(client_id, num):
    if client_id not in clients_dic:
        clients_dic[client_id] = {num: []}
    elif num not in clients_dic[client_id]:
        clients_dic[client_id][num] = []
    print(list(clients_dic.keys()))
    print(list(clients_dic[client_id].keys()))


def insert_updates(client_id, num, src_path, event, dst_path):
    for key in clients_dic[client_id]:
        if key != num:
            if dst_path is None:
                clients_dic[client_id][key].append([event, src_path])
            else:
                clients_dic[client_id][key].append([event, src_path, dst_path])


def delete_path(src_path):
    if os.path.isdir(os.path.dirname(src_path)):
        if not os.listdir(os.path.dirname(src_path)):
            os.rmdir(os.path.dirname(src_path))
        else:
            for sub in src_path.iterdir():
                if sub.is_dir():
                    delete_path(sub)
                else:
                    os.remove(os.path.basename(sub))
    else:
        os.remove(os.path.basename(src_path))


def delete_updates(client_id, num, event, src_path, dst_path):
    updates_list = clients_dic[client_id][num]
    wanted_update = [event, src_path, dst_path]
    for update in updates_list:
        if update == wanted_update:
            updates_list.pop(wanted_update)
            print('deleted:')
            print(update)


def init_clients_folder():
    os.mkdir(os.path.abspath('Clients'))
    return os.path.abspath('Clients')


def create_new_client_id(num):
    client_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))
    os.mkdir(os.path.join(os.path.abspath('Clients'), client_id))
    print(client_id)
    add_to_dic(client_id, num)
    return client_id


def create_socket(path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen()
    while True:
        client_socket, client_address = s.accept()
        with client_socket, client_socket.makefile('rb') as file:
            data = file.readline().strip().decode()
            print(data)
            if data == 'add my folder':
                num = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))
                client_socket.sendall(num.encode() + b'\n')
                client_id = create_new_client_id(num)
                client_socket.sendall(client_id.encode() + b'\n')
                folder_path = path + '/' + str(client_id)
                pull_data(folder_path, client_socket)

            elif data == 'update me':
                client_id = file.readline().strip().decode()
                print('client id:' + client_id)
                client_number = file.readline().strip().decode()
                print('client number:' + client_number)
                length = len(clients_dic[client_id][client_number])
                print(length)
                if length == 0:
                    client_socket.sendall(str(-1).encode() + b'\n')
                    client_socket.close()
                    continue
                client_socket.sendall((str(length)).encode() + b'\n')
                for i in range(length):
                    for j in range(3):
                        client_socket.sendall(clients_dic[client_id][client_number][i][j].encode() + b'\n')
                        print('sent ' + clients_dic[client_id][client_number][i][j])

            elif data == 'created':
                client_number = file.readline().strip().decode()
                src_path = file.readline().strip().decode()
                insert_updates(client_id, client_number, src_path, data, None)
                pull_data(os.path.abspath('Clients') + '/' + src_path, client_socket)
                print('pulled data')

            elif data == 'deleted':
                client_number = file.readline().strip().decode()
                src_path = file.readline().strip().decode()
                insert_updates(client_id, client_number, src_path, data, None)
                delete_path(src_path)
                print('deleted path')

            elif data == 'moved':
                client_number = file.readline().strip().decode()
                src_path = file.readline().strip().decode()
                dst_path = file.readline().strip().decode()
                insert_updates(client_id, client_number, src_path, data, dst_path)
                pull_data(dst_path, client_socket)
                delete_path(src_path)
                print('moved path')

            elif data == 'modified':
                client_number = file.readline().strip().decode()
                src_path = file.readline().strip().decode()
                insert_updates(client_id, client_number, src_path, data, None)
                pull_data(src_path, client_socket)
                delete_path(src_path)
                print('modified path')

            else:
                num = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))
                print(num)
                add_to_dic(client_id, num)
                client_socket.sendall(num.encode() + b'\n')
                push_data(os.path.abspath('Clients') + '/' + data, client_socket)

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