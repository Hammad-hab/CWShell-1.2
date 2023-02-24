from Socket import CW_SOCKET_C
from CommandLet import Interpreter


def generate_client_using_host(host):
    client = CW_SOCKET_C()
    mode = "STD"

    port = input("Enter PORT: ")
    connected = client.connect(host, int(port.strip()))
    # check if the server allowed this machine to connect
    if connected is None:
        # send the name of this machine
        client.send('{}'.format(client.name))
        intp = Interpreter(client)
        intp.start()
    else:
        raise Exception("Failed to connect")
