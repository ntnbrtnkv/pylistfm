import json
from copy import deepcopy
from pylistfm.modes import string_to_mode


default_filename = 'config.json'


class Config:
    def load(self, filename=default_filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            self._init(data)
        return self

    def to_json(self):
        json_o = deepcopy(self)
        del json_o.pylistfm.mode
        return json.dumps(json_o, default=lambda o: o.__dict__, indent=4)

    def _init(self, data):
        main = data['pylistfm']
        self.pylistfm = type('', (), {})()
        for key, value in main.items():
            setattr(self.pylistfm, key, value)
        setattr(self.pylistfm, 'mode', string_to_mode(self.pylistfm.default_mode))

        self.api = data['api']

    def init(self):
        data = {
            "pylistfm": {
                "dir": "D:/Music",
                "types": [
                    "mp3",
                    "flac"
                ],
                "default_mode": "s",
                "search_missing_albums": False,
                "limit": 50,
                "sources": [
                    "lastfm"
                ]
            },
            "api": {
                "lastfm": {
                    "key": "YOU_API_KEY_HERE"
                }
            }
        }
        self._init(data)

    def save(self, filepath=default_filename):
        with open(filepath, 'w') as outfile:
            outfile.write(self.to_json())
