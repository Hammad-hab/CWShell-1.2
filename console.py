# some global things all sub-files will use

from rich.console import Console
from termcolor import colored as color
import socket

console = Console()
hostName = socket.gethostname()


def scan_network():

    ...
