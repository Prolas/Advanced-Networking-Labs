import socket
import struct
import argparse


def main(group: str, port: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to all interfaces, NOT the multicast group!
    client.bind((group, port))

    # Join multicast group
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    try:
        while True:
            data = client.recv(1024)  # read full packets
            print(data.decode().strip(), flush=True)
    except KeyboardInterrupt:
        print("Receiver stopped.")
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("group", type=str)
    parser.add_argument("port", type=int)
    args = parser.parse_args()

    main(args.group, args.port)
