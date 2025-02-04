"""Example of api source

Package should have 'API' class with public 'get_top_tracks' method
"""


class API:
    def __init__(self, config=None):
        """Initialize your API

        :param config: all parameters needed for the API"""
        self.config = config

    def get_top_tracks(self, artist_name, mbid, limit=10):
        """Get most played/rated artist's tracks
        :return [('Track Name 1', 'Album Name 1'), ('Track Name 2', 'Album Name 2'), ...]

        :param artist_name: Artist name, etc. band or whatever
        :param mbid:        Music Brainz ID
        :param limit:       Limit returning top tracks number
        """
        return [('Track Name 1', 'Album Name 1'), ('Track Name 2', 'Album Name 2')]
