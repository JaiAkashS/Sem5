import socket
target_website = "www.msec.edu.in"
tcp_port = 80
# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((target_website, tcp_port))
# Send HTTP GET request
http_request = "GET / HTTP/1.1\r\nHost: " + target_website + "\r\n\r\n"
tcp_socket.sendall(http_request.encode())
# Receive and print response
http_response = b''
while True:
    data = tcp_socket.recv(4096)
    if not data:
        break
    http_response += data
# Decode and print the response
result = http_response.decode()
print(result)
# Close the socket
tcp_socket.close()
