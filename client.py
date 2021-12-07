import os
import socket
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
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
    with sock, sock.makefile('rb') as file:
        sock.sendall(b'add my folder\n')
        my_id = file.readline().strip().decode()
        push_data(folder_path, sock)
        return my_id


def pull_folder_from_server(sock, my_path, folder_name):
    with sock:
        sock.sendall(folder_name.encode() + b'\n')
        pull_data(my_path, sock)


def create(src_path):
    sock = connect_to_server(ip_server, port_server)
    sock.sendall('created'.encode() + b'\n')
    sock.sendall(src_path.encode() + b'\n')
    push_data(src_path, sock)


def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    create(event.src_path)


def delete(src_path):
    sock = connect_to_server(ip_server, port_server)
    sock.sendall('deleted'.encode() + b'\n')
    sock.sendall(src_path.encode() + b'\n')


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")
    delete(event.src_path)


def on_modified(event):
    pass
#     print(f"hey buddy, {event.src_path} has been modified")
#     sock = connect_to_server(ip_server, port_server)
#     if ((str(event.src_path).split('//'))[-1])[0] == '.':
#         if event.event_type != 'moved':
#             return


def move(src_path, dest_path):
    sock = connect_to_server(ip_server, port_server)
    sock.sendall('moved'.encode() + b'\n')
    sock.sendall(src_path.encode() + b'\n')
    sock.sendall(dest_path.encode() + b'\n')
    push_data(src_path, sock)


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    if ((str(event.src_path).split('//'))[-1])[0] == '.':
        if event.event_type != 'moved':
            return
    move(event.src_path, event.dest_path)


def check_for_updates():
    sock = connect_to_server(ip_server, port_server)
    with sock, sock.makefile('rb') as file:
        sock.sendall('update me\n'.encode())
        sock.sendall(client_id.encode() + b'\n')

        length = int(file.readline().strip().decode())
        for i in range(length):
            update_type = file.readline().strip().decode()
            update_src_path = file.readline().strip().decode()
            update_dst_path = file.readline().strip().decode()
            if update_type == 'created':
                create(update_src_path)
            elif update_type == 'deleted':
                delete(update_src_path)
            elif update_type == 'moved':
                move(update_src_path, update_dst_path)


if __name__ == '__main__':
    ip_server = sys.argv[1]
    port_server = int(sys.argv[2])
    path = sys.argv[3]
    timer = int(sys.argv[4])
    s = connect_to_server(ip_server, port_server)
    if len(sys.argv) == 6:
        client_id = sys.argv[5]
        pull_folder_from_server(s, path, client_id)

    else:
        client_id = push_folder_to_server(s, path)
    s.close()

    # the file patterns we want to handle
    patterns = ["*"]
    # contains the patterns that we don’t want to handle
    ignore_patterns = None
    # boolean that we can set to True if we want to be notified just for regular files (not for directories)
    ignore_directories = False
    # boolean that if set to “True”, made the patterns we previously introduced “case sensitive”
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(timer)
            check_for_updates()
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()



