import os
import random
import socket
import string


# pull to my folder
import time

def pull_data(path, s):
    with s, s.makefile('rb') as file:
        number_files = int(file.readline().strip().decode())
        print(number_files)
        for i in range(number_files):
            file_name = file.readline().strip().decode()
            if file_name.endswith(',isdir'):
                name, isdir = file_name.split(',')
                new_path = create_inner_folder(name, path)
                print(new_path)
                pull_data(new_path, s)
            else:
                file_size = int(file.readline().strip().decode())
                data = file.read(file_size)
                with open(os.path.join(path, file_name), 'wb') as f:
                    f.write(data)


def push_data(path, s):
    with s:
        files = os.listdir(path)
        s.sendall(str(len(files)).encode() + b'\n')
        time.sleep(1)
        for file in files:
            print(file)
            relative_file = os.path.join(path, file)
            if os.path.isdir(relative_file):
                s.sendall(file.encode() + b',isdir' + b'\n')
                time.sleep(1)
                push_data(relative_file, s)
            else:
                file_size = os.path.getsize(relative_file)
                s.sendall(file.encode() + b'\n')
                time.sleep(1)
                s.sendall(str(file_size).encode() + b'\n')
                time.sleep(1)
                with open(relative_file, 'rb') as f:
                    s.sendall(f.read())
                    time.sleep(1)


def create_inner_folder(name, path):
    os.mkdir(os.path.join(path, name))
    return os.path.join(path, name)

