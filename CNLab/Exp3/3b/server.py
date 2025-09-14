import socket

server_ip = 'localhost'
port = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, port))

while True:
    response = client.recv(1024)
    print("\nReceived >>>", response.decode())

    message = input('Enter text: ')
    message = message.encode()
    client.send(message)
    print('[+] Message sent')
