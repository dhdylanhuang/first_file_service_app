import socket
import sys
import os

# Import functions from an parent folder
sys.path.append('..')
from functions import send_file, recv_file, recv_listing

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server address and port from the command line 
try:
    server_address = (sys.argv[1], int(sys.argv[2]))
    server_address_str = str(server_address)

except ValueError:
    print("Invalid port number. Please enter a valid port number.")
    sys.exit(1) #exit(1) indicates program closes with an error

# Attempt to establish connection
try:
    print(f"Connecting to {server_address_str}")
    client_socket.connect(server_address)
    print(f"Connection Succesful")
    
except socket.error as e:
    print(f"Connection error: {e}. Please try again with a different port.")
    sys.exit(1)


try:
    # Get the function needed and filename 
    action = sys.argv[3].upper()
    filename = sys.argv[4]

    # Create request message and send to server
    request_m = f"{action} {filename}"
    client_socket.send(request_m.encode("utf-8"))

    # Handle file upload request
    if action == 'PUT':
        print("Attempting to upload file to the server...")
        response = client_socket.recv(1024).decode("utf-8") # Response from server if file exists or not 

        if response == "File already exists":
            print(f"Upload failed. {filename} already exists on server")
        elif response == "New file":
            client_socket.send(f'PUT {filename}'.encode("utf-8"))
            send_file(client_socket, filename)
            print("File successfully uploaded")
        else:
            print("Unexpected response from server.")

    # Handle download requests, refusing if file already exists
    elif action == 'GET':
        print("Attempting to download file from server...")

        if os.path.isfile(filename):
            client_socket.send("File already exists".encode("utf-8"))
            print(f"Download failed. {filename} already exists on server")
        else:
            client_socket.send("New file".encode("utf-8"))
            recv_file(client_socket, filename)
            print("File successfully downloaded")

    # Receives listing 
    elif action == 'LIST':
        client_socket.send('LIST'.encode("utf-8"))
        recv_listing(client_socket)
    else:
        print("Invalid operation")

# In the event of a connection drop 
except Exception as e:
    print(f"Request failed: {e}. Please check server status.")
    sys.exit(1)

finally:
    client_socket.close()
    sys.exit(0) # exit(0) to indicate programme closed without error