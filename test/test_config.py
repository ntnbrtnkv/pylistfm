import unittest
from pylistfm.config import Config


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_init(self):
        self.config.init()

        self.assertEqual(self.config.pylistfm.dir, 'D:/Music')
        self.assertEqual(self.config.pylistfm.types, ["mp3", "flac"])
        self.assertEqual(self.config.pylistfm.search_missing_albums, False)
        self.assertEqual(self.config.pylistfm.limit, 50)
        self.assertEqual(self.config.api['lastfm']['key'], 'YOU_API_KEY_HERE')

    def test_load(self):
        self.config.load()

        self.assertEqual(self.config.pylistfm.search_missing_albums, True)

    def test_tojson(self):
        self.config.init()
        json_string = self.config.to_json()

        self.assertEqual(json_string, """{
    "pylistfm": {
        "dir": "D:/Music",
        "types": [
            "mp3",
            "flac"
        ],
        "default_mode": "s",
        "search_missing_albums": false,
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
}""")
