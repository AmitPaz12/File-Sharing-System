import os
import random
import socket
import string


# pull to my folder
def pull_data(path, s):
    number_files = s.recv(4).decode()
    for i in range(number_files):
        protocol_size = s.recv(4).decode()
        file_name, size = s.recv(protocol_size).decode().split(',')
        file_size = int(size)
        complete_name = os.path.join(path, file_name)
        new_file = open(complete_name, "w")
        while new_file.tell() <= file_size:
            new_file.write(s.recv(1024).decode())
        new_file.close()


def push_data(path, s):
    number_files = len([f for f in os.listdir(path)])
    s.send(f"{str(number_files)}".encode())

    for file in os.listdir(path):
        relative_file = path + '/' + str(os.path.basename(file))
        protocol = str(os.path.basename(relative_file)) + ',' + str(os.stat(relative_file))
        len_protocol = len(protocol)
        s.send(bytes(len_protocol))
        s.send(protocol.encode())
        f = open(os.path.abspath(relative_file), 'r')

        # s.send(f"{str(os.path.basename(file))}{','}{str(os.path.getsize(file))}".encode())
        # s.send(f"{str(os.path.getsize(file))}{','}".encode())
        while True:
            data = f.read(1024)
            while data:
                s.send(data.encode())
                data = f.read(1024)
            break

        # s.send(f"{open(os.path.abspath(path), 'r')}{','}".encode())




