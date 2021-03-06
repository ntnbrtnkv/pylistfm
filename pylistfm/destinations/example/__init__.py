"""Example of api destination

Package should have 'API' class with public 'save' and 'process_missing_albums' methods
"""


class API:
    def __init__(self, pylistfm_config, api_config):
        """Initialize your API

        :param pylistfm_config: common parameters
        :param api_config: current API specific parameters"""
        pass

    def save(self, playlist_name, track_list, **kwargs):
        """Processes saving tracks as playlist somewhere

        :param playlist_name: playlist name to store
        :param track_list: list of instances pylistfm.Track api should use for creating playlist
        :param kwargs: additional parameters for current api
        """
        pass

    def process_missing_albums(self, track_list, **kwargs):
        """Process of alerting to user about albums destination doesn't have

        :param track_list: list of instances pylistfm.Track some of which have 'is_found' property False
        :param kwargs: additional parameters for current api
        """
        pass
