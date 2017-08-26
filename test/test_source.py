import unittest
from pylistfm.sources.lastfm import API as LastFMAPI
from pylistfm.sources.example import API as ExampleAPI
from pylistfm.config import Config


class SourceTests(unittest.TestCase):

    def test_example_api(self):
        example_api = ExampleAPI()
        res = example_api.get_top_tracks('Artist Name', 2)
        self.assertEqual(res, [('Track Name 1', 'Album Name 1'), ('Track Name 2', 'Album Name 2')])

    def test_lastfm_api(self):
        config = Config().load()
        lastfm_api = LastFMAPI(config.api['lastfm'])
        res = lastfm_api.get_top_tracks('ария', 4)
        self.assertEqual(res, [('Беспечный ангел', 'Tribute to harley-davidson'),
                               ('Улица роз', 'Герой асфальта'),
                               ('Осколок Льда', 'Химера'),
                               ('Штиль', 'Химера')])
