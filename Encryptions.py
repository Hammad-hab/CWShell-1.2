import base64


class ED:
    def __init__(self, name) -> None:
        self.enc_registery = {
            "CWCEAL": self.CWCEAL,
            "CWCEAL_L": self.CWCEAL_L
        }
        self.definations = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
        if not name in self.enc_registery:
            raise ValueError(
                f"{name} is not a defined encryption!\nAvailable Encryptions:\n    * CWCEAL (ClockWatch Custion Encryption ALgorithm)\n    * CWCEAL_L (ClockWatch Custion Encryption ALgorithm Large)")
            ...
        self.c = self.enc_registery[name]
        pass

    def __call__(self, text):
        rt = self.c(text)
        return rt

    def CWCEAL(text): ...
    def CWCEAL_L(text): ...


class Encryption(ED):
    def __init__(self, name) -> None:
        super().__init__(name)

    def CWCEAL(self, text):
        "Recomended"
        text = bytes(text, "utf-8")
        enx = base64.b16encode(text)
        enx = base64.b64encode(enx)
        enx = base64.a85encode(enx)
        return enx

    def CWCEAL_L(self, text: str):
        """
        Not Recomended
        It is awfully large in size
        """
        nstring = ""
        for char in text:
            char = "%" + str(self.definations.index(char.lower())
                             ) if char.lower() in self.definations else r"?"
            nstring += char + "••"
        return bytes(nstring, "utf-8")

        ...


class Decryption(ED):
    def __init__(self, name) -> None:
        super().__init__(name)

    def CWCEAL(self, text: bytes):
        enx = base64.a85decode(text)
        enx = base64.b64decode(enx)
        enx = base64.b16decode(enx)

        # enx = enx.decode("utf-8")
        return enx
        ...

    def CWCEAL_L(self, text: bytes):
        o_string = text.decode("utf-8").split("••")
        n_string = ""
        for char in o_string:
            if char != "?":
                char = char.replace("%", "").strip()
                try:
                    find = self.definations[int(char)]
                except:
                    find = " "
                n_string += find
            else:
                char = " "
                n_string += char
        return n_string
