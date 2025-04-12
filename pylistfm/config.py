import json
from copy import deepcopy
from pylistfm.modes import string_to_mode


default_filename = 'config.json'


class Config:
    def load(self, filename=default_filename):
        self._filename = filename
        with open(filename) as json_file:
            data = json.load(json_file)
            self._init(data)
        return self

    @property
    def filename(self):
        return self._filename

    def to_json(self):
        json_o = deepcopy(self)
        del json_o.pylistfm.mode
        return json.dumps(json_o, default=lambda o: o.__dict__, indent=4)

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

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
                "destinations": [
                    "local"
                ],
                "cache": ".cache",
                "default_mode": "s",
                "search_missing_albums": False,
                "limit": 50,
                "sources": [
                    "lastfm"
                ]
            },
            "api": {
                "lastfm": {
                    "key": "YOU_API_KEY_HERE",
                    
                    "Source of getting top tracks, artist is got by API anyway": "html,api",
                    "source": "html",
                    
                    "Date range for top tracks": "LAST_7_DAYS,LAST_30_DAYS,LAST_90_DAYS,LAST_180_DAYS,LAST_365_DAYS,ALL",
                    "date_preset": "LAST_365_DAYS",
                },
                "local": {
                    "dir": "D:/Music",
                    "types": [
                        "mp3",
                        "flac",
                        "mp4",
                        "m4a",
                        "wv"
                    ],
                    "playlist_type": "m3u"
                }
            }
        }
        self._init(data)

    def save(self, filepath=default_filename):
        with open(filepath, 'w') as outfile:
            outfile.write(self.to_json())
