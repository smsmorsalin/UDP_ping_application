import socket

SERVER_IP = "10.0.2.2"
SERVER_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((SERVER_IP, SERVER_PORT))

print(f"UDP Ping Server listening on {SERVER_IP}:{SERVER_PORT}")

while True:
    data, client_address = sock.recvfrom(1024)

    message = data.decode()

    print(
        f"Received: '{message}' "
        f"from {client_address[0]}:{client_address[1]}"
    )

    reply = f"Reply: {message}"

    sock.sendto(
        reply.encode(),
        client_address
    )
