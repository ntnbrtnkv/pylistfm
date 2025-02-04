import logging
import importlib
import datetime
from .sound_utils import Track
from .utils import validate_uuid4, CacheSource


class Playlist:
    def __init__(self, config, api_config=None):
        self._logger = logging.getLogger('pylistfm')
        self.config = config
        self.api_config = api_config
        self._sources = {}
        self._destinations = {}
        self._init_sources()
        self._init_destinations()

    def _init_destinations(self):
        self._logger.info("Initializing destinations")
        for _module in self.config.destinations:
            api = getattr(importlib.import_module('pylistfm.destinations.{0}'.format(_module)), 'API')
            self._destinations[_module] = api
            self._logger.info("Destination api {0} added".format(_module))

    def _init_sources(self):
        self._logger.info("Initializing sources")
        for _module in self.config.sources:
            api = getattr(importlib.import_module('pylistfm.sources.{0}'.format(_module)), 'API')
            self._sources[_module] = api
            self._logger.info("Source api {0} added".format(_module))

    def _get_tracks(self, artist, mbid):
        config = self.config
        result = {}
        cache = None
        if (config.cache is not None):
            cache = CacheSource(config.cache)
        # TODO: place for paralleling
        for module_name, api in self._sources.items():
            request_result = None
            if (cache is not None and cache.has(module_name, artist)):
                self._logger.info("Found cache for {0}".format(module_name))
                request_result = cache.get(module_name, artist)
            else:
                self._logger.info("Trying to get track from api {0}".format(module_name))
                request_result = api(self.api_config[module_name]).get_top_tracks(artist, mbid, config.limit)
                self._logger.info("Got tracks from api {0}".format(module_name))
                if (cache is not None):
                    cache.save(module_name, artist, request_result)
            required_tracks = list(map(lambda it: Track(it[0], it[1]), request_result))
            result[module_name] = required_tracks
        return result

    def create_playlist(self, artist, output=None, mbid=None):
        now = datetime.datetime.now()
        now_date = now.strftime("%Y-%m-%d")
        actual_artist = None

        # Founding all possible files by name and ID3 tags
        modules_tracks = self._get_tracks(artist, mbid)
        if validate_uuid4(artist):
            actual_artist = output
        else:
            actual_artist = artist

        # TODO: place for paralleling
        for s_module, track_list in modules_tracks.items():
            for d_module, api in self._destinations.items():
                instance = api(self.config, self.api_config[d_module])
                instance.save(now_date, track_list, artist=actual_artist)
