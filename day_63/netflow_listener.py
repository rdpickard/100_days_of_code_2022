import netflow
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 2055))
while True:
    payload, client = sock.recvfrom(4096)  # experimental, tested with 1464 bytes
    p = netflow.parse_packet(payload)  # Test result: <ExportPacket v5 with 30 records>
    print(p.header.version)  # Test result: 5
    print(p.flows)