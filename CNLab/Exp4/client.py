import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = "localhost"
port = 5858

domain = input("Enter domain name: ")
client_socket.sendto(domain.encode(), (host, port))

data, _ = client_socket.recvfrom(1024)

print(f"IP Address: {data.decode()}")

client_socket.close()

