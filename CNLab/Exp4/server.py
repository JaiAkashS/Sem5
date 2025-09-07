import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("localhost", 5858))
print(f"DNS Server running on 127.0.0.1:5858")

dns_table = {
    "example.com": "93.184.216.34",
    "google.com": "142.250.183.14",
    "yahoo.com": "98.137.11.163"
}

while True:
    data, addr = server_socket.recvfrom(1024)
    domain = data.decode().strip()
    
    print(f"Received query for {domain} from {addr}")
    ip = dns_table.get(domain, "Domain not found")

    server_socket.sendto(ip.encode(), addr)
