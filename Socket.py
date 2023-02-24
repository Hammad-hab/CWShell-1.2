import socket
import random
import math
from OptReader import CW_OPT_READER
from console import console, color
from Encryptions import Encryption, Decryption
from threading import Thread

PORT = 2000


class CW_SOCKET_S:
    def __init__(self, settings: CW_OPT_READER) -> None:
        # socket information
        self.family = socket.AF_INET
        self.type = socket.SOCK_STREAM
        self.name = socket.gethostname()
        self.host = socket.gethostbyname(self.name)
        self.encryption = settings.encryption
        self.mxbytes = settings.maxbytes
        # picking a random number from range(5000) for the port
        self.port = PORT
        # binding the address & creating the socket
        self.address = (self.host, self.port)
        self.socket = socket.socket(self.family, self.type)
        self.__bind__()
        # about the settings
        self.connected_clients = 0
        self.settings = settings
        self.clients = []
        self._onconnect = lambda *args: print(args)
        pass

    def onconnect(self, func):
        self._onconnect = func
        return
        ...

    def send(self, message: str):
        enc = Encryption(self.settings.encryption)
        encd = enc(message)
        self.socket.send(encd)
        ...

    def recive(self):
        dec = Decryption(self.settings["encryption"])
        decd = dec(self.socket.recv(self.settings.maxbytes))
        return decd
        ...

    def kill(self):
        self.socket.close()

    def listen(self):
        try:
            self._listen()
        except KeyboardInterrupt:
            self.socket.close()
            exit()
        ...

    def __bind__(self):
        try:
            self.socket.bind(
                self.address
            )
        except:
            try:
                print(color(f"PORT {self.port} is not vacant.", "red"))
                self.port = int(
                    input("Enter replacement port [2000-5000]: ").strip())
                self.address = (self.address[0], self.port)
                self.__bind__()
            except Exception as e:
                print(color("Program terminated due to the following error: ", "red"))
                print(color(f" → {e!r}", "red", attrs=["bold"]))
                exit()

    def _listen(self):
        self.socket.listen()
        # LOGS!
        console.log(
            f"Server started on {self.address[0]}:{self.address[1]} with {self.connected_clients} clients")
        while True:
            try:
                connection, address = self.socket.accept()
                # if the client address is not in the white list (specified in settings.json): ...
                if not address[0] in self.settings.whitelist or self.connected_clients >= self.settings.maxclients:
                    #  ...then...
                    connection.send(bytes("DENIED", "utf-8"))
                    connection.close()
                else:
                    # ...else...
                    # updating the number of clients and...
                    self.connected_clients += 1
                    # appending them to a list so that they can be accessed later
                    self.clients.append(
                        (connection, address, socket.gethostbyaddr(address[0])))
                    nclient = Thread(target=self._onconnect, args=(
                        (connection, address), self.connected_clients, self.clients))
                    nclient.start()

            # If the user is trying to quit the application with ^C then...
            except (Exception, KeyboardInterrupt) as e:
                # make sure that the socket is properly closed...
                self.socket.close()

                print("\n")
                # show logs...
                console.log("Exiting")
                print(color("Program terminated due to the following error: ", "red"))
                print(color(f" → {e!r}", "red", attrs=["bold"]))
                exit()
                # exit the application
    ...


class CW_SOCKET_C:
    def __init__(self) -> None:
        self.family = socket.AF_INET
        self.type = socket.SOCK_STREAM
        self.port = PORT
        self.name = socket.gethostname()
        self.socket = socket.socket(self.family, self.type)
        pass

    def connect(self, host, port):
        try:
            self.socket.connect((
                host,
                port
            ))

            data = self.socket.recv(1024).decode("utf-8")
            if data == "DENIED":
                return False
            a = data.split(",")
            a = [x.strip() for x in a]
            self.encryption = a[0]
            self.mxbytes = int(a[1])
            self.hostname = a[2]
        except Exception as e:
            self.kill()
            print(color("Program terminated due to the following error: ", "red"))
            print(color(f" → {e!r}", "red", attrs=["bold"]))
            exit()
        ...

    def send(self, message: str):
        enc = Encryption(self.encryption)
        encd = enc(message)
        self.socket.send(encd)
        ...

    def recive(self):
        dec = Decryption(self.encryption)
        decd = dec(self.socket.recv(self.mxbytes))
        return decd
        ...
        ...

    def kill(self):
        self.socket.close()


def create_sfunc_from_class(mclass: CW_SOCKET_C | CW_SOCKET_S, socket: socket.socket):
    enctype = mclass.encryption
    mbytes = mclass.mxbytes
    enc = Encryption(enctype)
    dec = Decryption(enctype)

    def send(str):
        encrypted = enc(str)
        socket.send(encrypted)
        return encrypted, str

    def recive():
        cntent = socket.recv(mbytes)
        dec_cntent = dec(cntent)
        return dec_cntent.decode("utf-8"), cntent

    def send_nodec(str):
        socket.send(bytes(str, "utf-8"))
        return

    return socket, send, recive, (enctype, mbytes, enc, dec), send_nodec
    ...
