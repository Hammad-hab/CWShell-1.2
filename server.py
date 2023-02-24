from Socket import CW_SOCKET_S, Decryption, Encryption, socket, create_sfunc_from_class, Thread
from OptReader import CW_OPT_READER
from console import color
from CommandLet import Interpreter


def start_Server(opt: CW_OPT_READER):
    # opt = CW_OPT_READER('settings.json')
    server = CW_SOCKET_S(opt)
    # server.port = 2022

    @server.onconnect
    def connected(cd, cno, cl):
        # The argument "cd" is the acrynom of "client data". It is a tuple which contains the socket and the socket's address.
        # The address itself is a tuple which contains the IP address of the socket and its port (the
        # port using which it connected to the server)
        client_r = cd[0]  # cd[0] will fetch the socket

        # Some extra information which is generally useless
        number_clients = cno
        all_clients = cl

        # create_sfunc_from_class is a function which takes in the server (or client, created using CW_SOCKET_S or CW_SOCKET_C)
        # and returns the socket (unaltered), the send function (which takes in a string and sends its encrypted form to a socket),
        # the receive function (recives maximum number of bytes specified and decrypts them) and some additonal data which is
        # also generally useless
        client, send, receive, data, send_ = create_sfunc_from_class(
            server, client_r)

        # Recive the name of the client
        send_(f"{opt.encryption}, {opt.maxbytes}, {socket.gethostname()}")
        client_name_, _ = receive()
        client_name = color(client_name_, "green")
        print(client_name, "connected")
        int = Interpreter(server)

        def terminal():
            running = True

            def brek():
                nonlocal running
                running = False
            while running:
                try:
                    msg, _ = receive()
                    int.read(msg, client_name, send, brek)
                except:
                    server.kill()
                    exit()
        terminal()

    server.listen()
    # dec = Decryption(opt.encryption)
    # enc = Encryption(opt.encryption)
