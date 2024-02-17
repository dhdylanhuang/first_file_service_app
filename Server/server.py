import socket
import sys
import os

# Import function from parent folder
sys.path.append('..')
from functions import send_file, recv_file, send_listing

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialising host and port 
host = '0.0.0.0' 
try:
    port = int(sys.argv[1])
except ValueError:
    print("Invalid port number. Please enter a valid port number.")
    sys.exit(1) # Flags 1 to indicate server closed with an error

# Bind the socket to the host and port and listen for incoming connections.
try:
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server up and running on {host}: {port}")
except socket.error as e:
    print(f"Connection error: {e}. Please try again with a different port.")
    sys.exit(1)

# Main loop to handle requests
while True:
    try:

        # Accepting an incoming connection
        print("Waiting for connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Receiving client request
        request = client_socket.recv(1024).decode("utf-8")
        print("Server commencing", request)
        print("...")
        request_parts = request.split()

        if not request:
            break # Exit if null request

        # Handle files uploaded to server, duplicate files are not allowed to be uploaded
        if request_parts[0] == 'PUT':
            filename = request_parts[1]
            print("Attempting to download file...")

            if os.path.isfile(filename):
                client_socket.send("File already exists".encode("utf-8"))
                print(f"Download failed. File already exists on server: {filename}")
            else:
                client_socket.send("New file".encode("utf-8")) 
                recv_file(client_socket, filename)
                print("File succefully downloaded")
            
        # Handle files downloaded from the server, duplicate files are not allowed to be uploaded
        elif request_parts[0] == 'GET':
            filename = request_parts[1]
            print("Attempting to upload file...")

            response = client_socket.recv(1024).decode("utf-8") # Receive client response whether file already exists or not
            if response == "File already exists.":
                print(f"Download failed. File already exists on client: {filename}")
            elif response == "New file":
                send_file(client_socket, filename)
                print("File succesfully uploaded")
            else:
                print("Unexpected response from server")

        # Handle listing requests
        elif request_parts[0] == 'LIST':
            print("Producing list of directories...")
            send_listing(client_socket)
            print("List succesfuly produced")
            
        # Handle invalid requests
        else:
            raise Exception("Invalid request: ", request_parts[0])
            
    # Handle connection issues
    except socket.error as e:
        print(f"Connection error: {e}. Please check client status.")
        sys.exit(1)

    except KeyboardInterrupt:
        print("Server interrupted. Shutting down...")
        break
    
    # Close the client socket when request has been handled
    finally:
        client_socket.close()


server_socket.close()
sys.exit(0) # Flag 0 to indicate server has closed without issue