import logging
import importlib
import datetime
from .sound_utils import Track


class Playlist:
    def __init__(self, config, api_config=None):
        logging.basicConfig(level=config.mode)
        self.config = config
        self.api_config = api_config
        self._sources = {}
        self._destinations = {}
        self._init_sources()
        self._init_destinations()

    def _init_destinations(self):
        logging.info("Initializing destinations")
        for _module in self.config.destinations:
            api = getattr(importlib.import_module('pylistfm.destinations.{0}'.format(_module)), 'API')
            self._destinations[_module] = api
            logging.info("Destination api {0} added".format(_module))

    def _init_sources(self):
        logging.info("Initializing sources")
        for _module in self.config.sources:
            api = getattr(importlib.import_module('pylistfm.sources.{0}'.format(_module)), 'API')
            self._sources[_module] = api
            logging.info("Source api {0} added".format(_module))

    def _get_tracks(self, artist):
        config = self.config
        result = {}
        # TODO: place for paralleling
        for module_name, api in self._sources.items():
            logging.info("Trying to get track from api {0}".format(module_name))
            request_result = api(self.api_config[module_name]).get_top_tracks(artist, config.limit)
            logging.info("Got tracks from api {0}".format(module_name))
            required_tracks = list(map(lambda it: Track(it[0], it[1]), request_result))
            result[module_name] = required_tracks
        return result

    def create_playlist(self, artist):
        now = datetime.datetime.now()
        now_date = now.strftime("%Y-%m-%d")

        # Founding all possible files by name and ID3 tags
        modules_tracks = self._get_tracks(artist)
        # TODO: place for paralleling
        for s_module, track_list in modules_tracks.items():
            for d_module, api in self._destinations.items():
                instance = api(self.config, self.api_config[d_module])
                instance.save(now_date, track_list, artist=artist)
