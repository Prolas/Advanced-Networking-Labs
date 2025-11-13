import socket
import ssl
import pprint
from datetime import datetime
from time import sleep
import subprocess
import re
import sys
import argparse

def format_print(data: bytes):
    data_line = data.decode()

    # Split the string on 'This is PMU data ' and reconstruct each line
    parts = data_line.split("This is PMU data ")
    
    for part in parts:
        if part.strip():  # skip empty parts
            print(f"This is PMU data {part.strip()}")


def main(server: str, port: int, command: str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, port))
    client.send(command.encode("utf-8"))
    counter = 0
    while(True):
        data = client.recv(1 << 10)
        if data:
            counter +=1
            format_print(data)
        else:
            #print(counter)
            return


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
    
    parser.add_argument(
        "command",
        help="either CMD_short:0 or CMD_short:1 or CMD_floodme",
        type=str,
    )
    
    args = parser.parse_args()

    main(args.server, args.port, args.command)
