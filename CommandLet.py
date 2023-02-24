from console import hostName, color, console
from threading import Thread
from Socket import CW_SOCKET_C, CW_SOCKET_S
import os

# these are some long classes that don't make any sense


class CMD_LET:
    def __init__(self, welcome=True) -> None:
        self.welcome_msg = CMD_LET.prepmsg() if welcome else None
        if welcome:
            print(self.welcome_msg)
        self.input = color(f"{hostName} → ", "green", attrs=["bold"])
        self.commands = []
        self.cwshell = True
        pass

    def help(self):
        print("this is 'help'")
        ...

    def start(self):
        thread = Thread(target=self._start)
        thread.start()

    def _start(self):
        try:
            while self.cwshell:
                command = input(self.input)
                for property in self.commands:
                        command_l = command.split(" ")
                        command_n = command_l[0].strip()
                        if command_n != property["name"]:
                            continue
                        else:
                            property["func"](*command_l[1:command_l.__len__()])
                            continue

        except Exception as e:
            print(color("Program terminated due to the following error: ", "red"))
            print(color(f" → {e!r}", "red", attrs=["bold"]))
            exit()

    def declare(self, function):
        self.commands.append({
            "name": function.__name__,
            "func": lambda *args: function(*args)
        })
        return

    @classmethod
    def prepmsg(cls):
        basic = color("Welcome to {} {}".format(
            color("CWShell", "green", attrs=["bold"]),
            color("v1.2 lTS", "blue", attrs=["bold"])
        ), "blue", attrs=["bold"]) + color(
            "\nFor more information type {}".format('\'help\''), 'blue', attrs=["bold"])

        return basic
        ...

    def switchmode(self):
        self.cwshell = False
        ...


class Interpreter:
    def __init__(self, mclass: CW_SOCKET_C | CW_SOCKET_S) -> None:
        self.running = True
        self.klass = mclass
        self.mode = "STD"
        self.modes = ["STD", "BASH", "PYTHN", "CWSHELL"]
        self.restricted_modes = ["BASH", "PYTHN"]
        self.mode_recogniser = "$"
        ...

    def start(self):
        while self.running:
            ftext = input(
                f"{self.klass.hostname} with mode {self.mode} @ ").strip()
            if ftext.strip() == "exit":
                self.klass.send("👋🏻")
                rc = self.klass.recive().decode("utf-8")

                self.klass.kill()
                exit()
            else:
                self.klass.send(f"{ftext}")

            if ftext[1:ftext.__len__()].strip() in self.modes:
                print("Waiting for the server to respond...")
                res = self.klass.recive().decode("utf-8")
                if res == "P":
                    self.mode = ftext[1:ftext.__len__()].strip()
                    print("Successfully swictched mode")
                else:
                    print("Host refused")
        ...

    def read(self, cmd: str, cname, send, breakr):
        command = cmd
        if command == "👋🏻":
            breakr()
            send("OK")
            ...
        if command == "$BASH":
            if self.klass.settings["userrights"] != "*":
                permission = input(f"{cname} wants to switch to BASH mode [Y/N] ")
                if permission.upper()[0] == "Y":
                    self.mode = "BASH"
                    print(cname, "switched to BASH mode")
                    send("P")
                else:
                    send("N")
            else:
                send("P")
                self.mode = "BASH"
                print(cname, "switched to BASH mode")
                
                ...
        elif command == "$STD":
            self.mode = "STD"
            send("P")

        else:
            if self.mode == "STD":
                print(cname, "says", command)
            elif self.mode == "BASH":
                print(cname, "executed", command)
                os.system(command)
            else:
                print("....")
            ...
