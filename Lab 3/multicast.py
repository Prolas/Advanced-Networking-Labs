import socket
import struct
import argparse

def main(group: str, port: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client.bind(('', port))  # '' listens on all interfaces

    # Tell the OS to add the socket to the multicast group
    # on all interfaces.
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    try:
        while True:
            data, addr = client.recvfrom(1024)
            print(data.decode().strip())
    except KeyboardInterrupt:
        print("\nReceiver stopped.")
    finally:
        client.close()
    


  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "group",
        help="the multicast group address on which to listen",
        type=str,
    )
    parser.add_argument(
        "port",
        help="port number of the server",
        type=int,
    )

    args = parser.parse_args()

    main(args.group, args.port)
