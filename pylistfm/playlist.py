import codecs
import glob
import logging
import importlib
import datetime
from pylistfm.utils import Utils
from pylistfm.sound_utils import Track, TrackUtils


class Playlist:
    def __init__(self, config, api_config=None):
        logging.basicConfig(level=config.mode)
        self.config = config
        self.api_config = api_config
        self.sources = {}
        self._init_sources()
        self._base_dir = ""

    def _init_sources(self):
        logging.info("Initializing sources")
        for source_module in self.config.sources:
            api = getattr(importlib.import_module('pylistfm.sources.{0}'.format(source_module)), 'API')
            self.sources[source_module] = api
            logging.info("Api {0} added".format(source_module))

    def _get_tracks(self, artist):
        config = self.config
        result = {}
        for module_name, api in self.sources.items():
            logging.info("Trying to get track from api {0}".format(module_name))
            request_result = api(self.api_config[module_name]).get_top_tracks(artist, config.limit)
            logging.info("Got tracks from api {0}".format(module_name))
            required_tracks = list(map(lambda it: Track(it[0], it[1]), request_result))
            result[module_name] = required_tracks
        return result

    def _find_local_tracks(self, track_list):
        config = self.config
        local_filepaths = []
        # Trying to find all files with given filetypes in base_dir with subdirs
        logging.info("Loading local music library")
        for _type in config.types:
            local_filepaths.extend(Utils.insensitive_glob(self._base_dir + '**/*.' + _type))
        local_files = TrackUtils.tracks_by_paths(local_filepaths)
        logging.info("Local music library has been loaded")

        for file in local_files:
            for track in track_list:
                track_name = track.lowered_title
                by_file = track_name in file.lowered_filename
                by_tag = False
                # If one of id3 titles same as given by api
                for title in file.id3_lowered_titles:
                    if track_name in title:
                        by_tag = True
                        break
                if by_file or by_tag:
                    if (not track.is_found_locally() or
                            track > file):
                        track.copy_fileinfo_from(file)
                    logging.info('Found song "{0}" in your collection'.format(track.title))

    def _find_missing_albums(self, track_list):
        config = self.config
        suggested_albums = set('')
        for track in track_list:
            if not track.is_found_locally():
                logging.warning('Not found song "{0} - {1}" in your collection\n'.format(track.title, track.album.title))
                if track.album is not None:
                    suggested_albums |= {track.album}
        return suggested_albums

    def create_playlist(self, artist):
        config = self.config
        self._base_dir = config.dir + "/*" + ''.join(map(Utils.either, artist)) + "*/"
        music_dir = glob.glob(self._base_dir)[0]
        now = datetime.datetime.now()
        now_date = now.strftime("%Y-%m-%d_")

        # Founding all possible files by name and ID3 tags
        modules_tracks = self._get_tracks(artist)

        for module_name, track_list in modules_tracks.items():
            self._find_local_tracks(track_list)
            # Founding missing albums
            if config.search_missing_albums:
                suggested_albums = self._find_missing_albums(track_list)
                self.save_missing_albums(music_dir + now_date + module_name + '_missing_albums', suggested_albums)

            self.save_m3u(music_dir + now_date + module_name + '_pylistfm.m3u', track_list, music_dir)

    def save_missing_albums(self, path_to_file, suggested_albums):
        if len(suggested_albums) > 0:
            logging.info('You may want to download this albums:')
            suggested_albums = list(suggested_albums)

            with codecs.open(path_to_file, 'w', 'utf-8') as f:
                for alb in suggested_albums:
                    print("\"{}\"".format(alb))
                    f.write(alb.title + '\n')

    def save_m3u(self, path_to_file, track_list, music_dir):
        logging.info("Saving m3u file: {}".format(path_to_file))
        with codecs.open(path_to_file, 'w', 'utf-8') as f:
            f.write(u'\ufeff#EXTM3U\n')
            for track in track_list:
                if track.is_found_locally():
                    f.write(track.relative_filepath(music_dir) + "\n")
        logging.info("Saving completed")
