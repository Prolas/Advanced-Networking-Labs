import socket
import argparse

# python3 PDC.py advnet.epfl.ch 5004
def wait_for(client: socket.socket, command: str):
    """Send command and wait for any response."""
    try:
        client.send(command.encode("utf-8"))
        data = client.recv(1024)  # buffer size increased
        print(data.decode() != "")
        return True
    except (TimeoutError, socket.error):
        #print("TO")
        return False


def create_socket(server: str, port: int, af) -> socket.socket:
    try:
        infos = socket.getaddrinfo(server, port, af, socket.SOCK_DGRAM)
        if not infos:
            return None
        ip_info = infos[0]
        sock = socket.socket(af, socket.SOCK_DGRAM)
        sock.connect(ip_info[4])
        sock.settimeout(0.5)
        return sock
    except Exception as e:
        print("Connection failed:", e)
        return None


def main(server: str, port: int):
    command = "RESET:20"
    n = 1
    global_count = 0

    client_ipv4 = create_socket(server, port, socket.AF_INET)
    client_ipv6 = create_socket(server, port, socket.AF_INET6)

    #print(client_ipv4)
    #print(client_ipv6)
    sock: None | socket.socket = None

    for i in range(n):
        count = 0
        success = False
        while not success:
            count += 1
            # if sock:
            #     success = wait_for(client_ipv4, command)
            #     if success:
            #         global_count += count
            #         break
            # else:
            # Try IPv4 first
            print("Try IPv4")
            success_ipv4 = wait_for(client_ipv4, command)
            if success_ipv4:
                print("IPv4")
                sock = client_ipv4
                global_count += count
            # Then try IPv6
            print("Try IPv6")
            success_ipv6 = wait_for(client_ipv6, command)
            if success_ipv6:
                print("IPv6")
                sock = client_ipv6
                global_count += count
            success = success_ipv4 or success_ipv6
                    

    print(
        f"Average number of trials: {global_count / n}, probability of success: {n / global_count}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("server", help="IPv4/IPv6 address or domain name", type=str)
    parser.add_argument("port", help="Port number of the server", type=int)
    args = parser.parse_args()

    main(args.server, args.port)
