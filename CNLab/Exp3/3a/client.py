import socket
# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
print('Chat started')
# Listen for up to 10 clients
server.listen(10)
# Accept a client connection
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connected to the server')
# Chat loop
while True:
    command = input('Enter text: ')
    command = command.encode()
    client.send(command)
    print('[+] Text sent')
