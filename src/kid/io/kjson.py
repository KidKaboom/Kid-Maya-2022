# :coding: utf-8

# Project Modules
from kid.core import KObject
from kid.io.kio import KIO, KIORoot


# Python Modules
import json


class Kjson(KIO):
    """ Class that handles reading and writing to .json files.
    """
    def extension(self):
        return ".json"

    def write_handler(self, *args, **kwargs):
        data = {
            "head": self.root.as_dict(),
            "data": self.data,
            }

        json.dump(data,
                  self.file(),
                  separators=(",", ":"),
                  indent=2,
                  )
        return

    def read_handler(self, *args, **kwargs):
        data = json.load(self.file())
        self.data = data.get("data", None)

        head = data.get("head", dict())

        for key in data.get("head", dict()):
            if hasattr(self.root, key):
                setattr(self.root, key, head[key])
        return


if __name__ == '__main__':
    from kid.core import kglobals, KPath

    _data = {"name": "Bob", "languages": ["English", "French"]}
    _path = KPath(kglobals.DATA_PATH) + "test.json"

    # _kson = Kjson.write(_path, _data)
    _kson = Kjson.read(_path)
    print(_kson.root)