import socket
import ssl
import pprint
from datetime import datetime
from time import sleep
import subprocess
import re
import sys
import argparse

# 4.8, 0.21
# 4.8 0.21

def wait_for(client: socket.socket, command: str):
    client.send(command.encode("utf-8"))
    try:
        data = client.recv(1 << 5)
        return True
    except TimeoutError as e:
        return False


def main(server: str, port: int):
    clientIpv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientIpv6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    clientIpv4.connect((server, port))
    clientIpv6.connect((server, port))
    clientIpv4.settimeout(1)
    clientIpv6.settimeout(1)

    SOCK: None | socket.socket = None

    command = "RESET:20"
    n = 1   
    global_count = 0
    for i in range(n):
        count = 0
        success = False
        if SOCK:
            while not success:
                count += 1
                success = wait_for(SOCK, command)
                if success:
                    print(f"{i}: {count}")
                    global_count += count

        else:
            while not success:
                count += 1
                success = wait_for(clientIpv4, command)
                if success:
                    SOCK = clientIpv4
                    print(f"IPv4: {count}")
                    global_count += count
                    break

                success = wait_for(clientIpv6, command)
                if success:
                    SOCK = clientIpv6
                    print(f"IPv6: {count}")
                    global_count += count
                    break

    print(
        f"Average number of trials: {global_count / n}, probabilty of success: {n /global_count}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "server",
        help="either the IPv4 address of the server or its domain name.",
        type=str,
    )
    parser.add_argument(
        "port",
        help="port number of the server",
        type=int,
    )

    args = parser.parse_args()

    main(args.server, args.port)
