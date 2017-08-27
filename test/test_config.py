import unittest
from pylistfm.config import Config


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_init(self):
        self.config.init()

        self.assertEqual(self.config.pylistfm.search_missing_albums, False)
        self.assertEqual(self.config.pylistfm.limit, 50)
        self.assertEqual(self.config.api['lastfm']['key'], 'YOU_API_KEY_HERE')
        self.assertEqual(self.config.api['local']['dir'], 'D:/Music')
        self.assertEqual(self.config.api['local']['types'], ["mp3", "flac"])

    def test_load(self):
        self.config.load()

        self.assertEqual(self.config.pylistfm.search_missing_albums, True)

    def test_tojson(self):
        self.config.init()
        json_string = self.config.to_json()
        self.maxDiff = None

        self.assertEqual(json_string, """{
    "pylistfm": {
        "destinations": [
            "local"
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
        },
        "local": {
            "dir": "D:/Music",
            "types": [
                "mp3",
                "flac"
            ],
            "playlist_type": "m3u"
        }
    }
}""")
