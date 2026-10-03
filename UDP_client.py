import socket
import time

SERVER_IP = "10.0.2.2"
SERVER_PORT = 5000

PING_COUNT = 10
TIMEOUT = 2

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.settimeout(TIMEOUT)

print(f"UDP Ping {SERVER_IP}:{SERVER_PORT}")
print()

sent = 0
received = 0

for sequence in range(1, PING_COUNT + 1):

    message = f"PING {sequence}"

    start_time = time.time()

    try:

        sock.sendto(
            message.encode(),
            (SERVER_IP, SERVER_PORT)
        )

        sent += 1

        data, server_address = sock.recvfrom(1024)

        end_time = time.time()

        rtt = (end_time - start_time) * 1000

        received += 1

        print(
            f"{data.decode()} "
            f"from {server_address[0]} "
            f"time={rtt:.2f} ms"
        )

    except socket.timeout:

        print(
            f"Request timeout for sequence {sequence}"
        )

    time.sleep(1)


print()
print("--- UDP Ping statistics ---")

packet_loss = ((sent - received) / sent) * 100

print(f"{sent} packets sent")
print(f"{received} packets received")
print(f"{packet_loss:.1f}% packet loss")

sock.close()
