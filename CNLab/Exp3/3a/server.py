import socket
server_ip = "localhost"
port = 8080
# Create socket and connect
bd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bd.connect((server_ip, port))
command = "open"
while command != "close":
    command = bd.recv(1024).decode()
    print("Received >>>", command)
bd.close()
