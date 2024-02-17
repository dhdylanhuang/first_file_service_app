import os

def send_file(socket, filename):
    try:
        with open(filename, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                socket.send(data)
    except Exception as e:
        print(f"Error while sending file: {e}")

def recv_file(socket, filename):
    try:
        with open(filename, 'wb') as file:
            while True:
                data = socket.recv(1024)
                if not data:
                    break
                file.write(data)
    except Exception as e:
        print(f"Error while receiving file: {e}")

def send_listing(socket):
    files = os.listdir('.')
    file_list = '\n'.join(files)
    socket.send(file_list.encode())

def recv_listing(socket):
    data = socket.recv(1024).decode()
    print("List of files/directories on the server:")
    print(data)

def terminate_connection(socket):
    return socket.close()