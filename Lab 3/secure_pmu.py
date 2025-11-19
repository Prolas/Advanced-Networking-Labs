import socket
import ssl
import argparse

HOST = "127.0.0.1"

# python3 secure_pmu.py certificate.crt 345665_key.pem 
# python3 Part5_PDC.py CMD_short:0 Part5_ca.crt
def main(port: int, certificate: str, key: str):
    n = 10
    # Create a standard TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, port))
    sock.listen(5)

    # Wrap the socket with SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certificate, keyfile=key)

    while True:
        client_socket, addr = sock.accept()
        try:
            # Wrap client socket with SSL
            tls_client = context.wrap_socket(client_socket, server_side=True)
            data = tls_client.recv(1024).decode("utf-8")
            print(f"Received: {data}")
            tls_client.send(b"Hello from TLS server!\n")
            for i in range(n):
                m = f"This is PMU data {i}!\n"
                tls_client.send(m.encode())

            tls_client.close()
        except ssl.SSLError as e:
            client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Port number of the server", type=int)
    parser.add_argument("certificate", help="path to your signed certificate", type=str)
    parser.add_argument("key", help="path to your secret key", type=str)

    args = parser.parse_args()

    main(args.port, args.certificate, args.key)
