import socket

# Create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(1)
print('Chat started.')

# Accept client connection
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connected to the server')

# Chat loop
while True:
    command = input('Enter text: ')
    command = command.encode()
    client.send(command)
    print('[+] Text sent')

    message = client.recv(1024)
    print("\nReceived >>>", message.decode())
