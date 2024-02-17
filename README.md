# first_file_service_app
Networks and Operating Systems Essentials 2, 1st Semester Assessed Exercise 1

Done using the Python socket library to create a simple, yet powerful, file service application. This app consists of two Python scripts, a "server" receives and serves client requests for files stored in a local directory, and a "client" that allows the user to upload/download files from the server, as well as list the files currently stored on the server side.

How to Run: 
1. The server is run on the terminal.
2. The server receives, as its single command line argument, its port number; that is, the server should be executed like so: python server.py <port /number> (remove the / e.g. M:\some_dir> python server.py 6789)
3. On a separate terminal run the client.
4. The client receives its arguments as command line arguments. The first argument is the address of the server (hostname or IP address) and the second argument is the server’s port number. The next argument should be one of “put”, “get” or “list”; these signify that the client wishes to send or receive a file, or request a directory listing, respectively. For “put” and “get” there should then be one more argument with the name of the file to upload/download respectively. That is, the client should be executed like so: python client.py <hostname> <port> <put filename|get filename|list> (e.g. M:\some_dir> python client.py localhost 6789 put test1.txt or M:\some_dir> python client.py localhost 6789 list)

The server handles 3 kinds of requests:
1. Uploading of a file: The client can include=the request type and the filename to be used on the server side, and the data of the file. The server then creates the file and copy the data sent by the client from the socket to the file. The server also denies overwriting existing files.
2. Downloading of a file: The client request includes the request type and the filename of the file to be downloaded. The server then opens the file (in binary mode) and copies its data to the client through the socket.
3. Listing of 1st-level directory contents: The client request indicates the request type. The server then constructs a list of the names of files/directories at the top level of its current working directory (using os.listdir()) and returns it to the client over the socket.

The client handles 3 kinds of requests:
1. Upload (“put”) request: The client opens (in binary mode) the local file defined on the command line, read its data, send it to the server through the socket, and finally closes the connection.
2. Download (“get”) request: The client creates the local file defined on the command line (in exclusive binary mode), reads the data sent by the server, stores it in the file, and finally closes the connection. The client also deny overwriting existing files.
3. Listing (“list”) request: the client sends an appropriate request message, receives the listing from the server, prints it on the screen one file per line, and finally closes the connection.
