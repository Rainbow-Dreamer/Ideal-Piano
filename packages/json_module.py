import json


class json_module:

    def __init__(self, file, text=None):
        if text is None:
            with open(file, encoding='utf-8') as f:
                text = json.load(f)
        self.json = text
        for i, j in self.json.items():
            setattr(self, i, j)
