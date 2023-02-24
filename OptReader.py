import json


class CW_OPT_READER:
    def __init__(self, file_name: str | bytes, /) -> None:
        self.file = file_name.strip()
        if not self.file.endswith(".json"):
            raise ValueError("Invalid file name")
        with open(self.file, "r+") as f:
            contents = f.read()
            contents_e = json.loads(contents)
            self._define_properties(contents_e)

    def _define_properties(self, contents):
        self.whitelist = contents["whitelist"]
        self.userrights = contents["userrights"]
        self.maxbytes = contents["maxbytes"]
        self.maxclients = contents["mxclients"]
        self.encryption = contents["encryption"]
        ...
    
    ...

