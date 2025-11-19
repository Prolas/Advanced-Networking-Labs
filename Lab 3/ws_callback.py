import websocket
import argparse
import rel

COUNT = 0
COMMAND = None
SENT = False

def on_message(ws, message):
    global COUNT
    COUNT += 1
    print(message.decode())


def on_error(ws, error):
    print("Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    global SENT
    print("Opened connection")
    if not SENT:
        ws.send(COMMAND)
        print(f"Sent: {COMMAND}")
        SENT = True


def main(server: str, port: int, command: str):
    global COMMAND
    global SENT 
    SENT = False
    COMMAND = command

    websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        f"ws://{server}:{port}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)
    rel.dispatch()
    
    print(COUNT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("server", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("command", type=str)
    args = parser.parse_args()

    main(args.server, args.port, args.command)
