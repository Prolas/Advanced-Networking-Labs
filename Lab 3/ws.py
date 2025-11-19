from websocket import create_connection
import argparse


def main(server: str, port:int, command: str):
    ws = create_connection(f"ws://{server}:{port}")
    print(f"Sent {command}")
    ws.send(command)
    print("Receiving...")
    result = ws.recv()
    while result:
        print(result.decode())
        result = ws.recv()
    
    ws.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("server", help="IPv4/IPv6 address or domain name", type=str)
    parser.add_argument("port", help="Port number of the server", type=int)
    parser.add_argument("command", help="the command to send ", type=str)

    args = parser.parse_args()

    main(args.server, args.port, args.command)