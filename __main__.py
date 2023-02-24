from CommandLet import CMD_LET
from console import hostName, socket, color
from Client import generate_client_using_host
from server import start_Server
from OptReader import CW_OPT_READER
import os
import json

cmd = CMD_LET()


@cmd.declare
def name(*args):
    def showhelp():
        print("""
name [-h/-f/-i]: displays the name if the machine
                * -h [--help] shows this prompt
                * -f [--full] shows the full bane of the machine
                * -i [--ipv4] shows the ip address of the current machine    
                
                """)
    try:
        if args[0] == "-h" or args[0] == "--help":
            showhelp()
        elif args[0] == "-f" or args[0] == "--full":
            print(hostName)
        elif args[0] == "-i" or args[0] == "--ipv4":
            print(socket.gethostbyname(hostName))
    except:
        showhelp()


@cmd.declare
def clear(*args):
    os.system("clear")


@cmd.declare
def connect(*args):
    def showhelp():

        print("""
connect [-n/-i]: connects to a server
                * -n [--name] connects to a server using its name (NOT RECOMENEDED IS SLOW)
                * -i [--ip] connects to a server using its ip address 
                
                """)
    try:
        if args[0] == "-n" or args[0] == "--name":
            target = socket.gethostbyname(args[1])
            try:
                generate_client_using_host(target)
            except Exception as e:
                print(color("Program terminated due to the following error: ", "red"))
                print(color(f" → {e!r}", "red", attrs=["bold"]))
                exit()
            # connect
            ...
        elif args[0] == "-i" or args[0] == "--ip":
            target = args[1]
            try:
                generate_client_using_host(target)
            except Exception as e:
                print(color("Program terminated due to the following error: ", "red"))
                print(color(f" → {e!r}", "red", attrs=["bold"]))
                exit()

            # connect using ip
            ...
    except Exception as e:
        print("Insufficent OR invalid Arguments. Expected the host name or host ip")
        showhelp()


@cmd.declare
def stserver(*args):

    if args.__len__() == 0:
        print("""
                stserver [settings.json]: makes your machine a sevrer to a server
                    * settings.json is a file which contains configuations
                    to generate this file from scratch type mkconfig
                """)
    else:
        try:
            OPT = CW_OPT_READER(args[0].strip()) 
        except Exception as e:
            print(color(f" → {e!r}", "red", attrs=["bold"]))
        else:
            start_Server(OPT)


@cmd.declare
def exit0(*args):
    exit()


@cmd.declare
def mkconfig(*args):
    print("Generating config file")
    rights = input("Enter user rights [*/ask]: ")
    mbytes = input(
        "Enter maximum amount of bytes that can be transfered [1-104,8576]: ")
    mclients = input(
        "Enter maximum number of clients allowed to connect [1-10,000]: ")
    encryption = input("Enter encryption style [CWCEAL/CWCEAL_L]: ")
    name = input("Enter configuration name (filename): ")
    dict_form = {
        "whitelist": [
            "127.0.0.1"
        ],
        "userrights": rights,
        "maxbytes": int(mbytes),
        "mxclients": int(mclients),
        "encryption": encryption
    }
    try:
        with open(name + ".json", "x") as f:
            content = json.dumps(dict_form)
            f.write(content)
            f.close()
    except Exception as e:
        print(
            color("Failed to make configuration file due to the following error: ", "red"))
        print(color(f" → {e!r}", "red", attrs=["bold"]))
    else:
        print("configuration successfully made!")



@cmd.declare
def quit(*args):
    exit()
    


cmd.start()
