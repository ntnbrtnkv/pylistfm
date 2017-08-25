import json
from pylistfm.modes import Modes


class Config:
    def __init__(self, filename='config.json'):
        with open(filename) as json_file:
            data = json.load(json_file)

            main = data['pylistfm']
            self.pylistfm = type('', (), {})()
            for key, value in main.items():
                setattr(self.pylistfm, key, value)
            setattr(self.pylistfm, 'mode', self.pylistfm.default_mode)
            # self.pylistfm.dir = main['dir']
            # self.pylistfm.types = main['types']
            # self.pylistfm.sources = main['sources']
            # self.pylistfm.max_songs = main['max_songs']
            # self.pylistfm.search_missing_albums = main['search_missing_albums']

            self.api = data['api']
