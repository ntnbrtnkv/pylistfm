from typing import List
import logging
import codecs
import glob
from .utils import Utils
from .sound_utils import TrackUtils, FileTrack


class API:
    def __init__(self, glob_config, api_config):
        self._config = glob_config
        self._logger = logging.getLogger('pylistfm')
        self._dir = api_config['dir']
        self._types = api_config['types']
        self._playlist_type = api_config['playlist_type']

    def save(self, playlist_name, track_list, **kwargs):
        artist = kwargs['artist']
        config = self._config
        self._base_dir = self._dir + "/*" + ''.join(map(Utils.either, artist)) + "*/"
        music_dir = glob.glob(self._base_dir)[0]

        files_tracks = list(map(lambda tr: FileTrack(tr), track_list))

        self._find_local_tracks(files_tracks)

        if config.search_missing_albums:
            self.process_missing_albums(files_tracks, path_to_file=music_dir + playlist_name + '_missing_albums')

        func = getattr(self, '_save_' + self._playlist_type)
        func(music_dir + playlist_name + '_pylistfm', files_tracks, music_dir)

    def _find_local_tracks(self, track_list: List[FileTrack]):
        local_filepaths = []
        # Trying to find all files with given filetypes in base_dir with subdirs
        self._logger.info("Loading local music library")
        for _type in self._types:
            local_filepaths.extend(Utils.insensitive_glob(self._base_dir + '**/*.' + _type))
        local_tracks = TrackUtils.tracks_by_paths(local_filepaths)
        self._logger.info("Local music library has been loaded")

        for track in track_list:
            lowered_track_title = track.title
            current_track = None
            for local_track in local_tracks:
                found = local_track.is_same_title(lowered_track_title)

                if found:
                    if current_track is None:
                        current_track = local_track
                    elif current_track < local_track:
                        current_track = local_track

            if current_track is not None:
                track.copy_info_from(current_track)
                self._logger.info('Found song "{0}" in your collection'.format(current_track.title))

    def _find_missing_albums(self, track_list: List[FileTrack]):
        suggested_albums = {}
        for ind, track in enumerate(track_list):
            if not track.is_found:
                self._logger.warning(
                    'Not found song [{}] "{} - {}" in your collection'.format(ind + 1, track.title, track.album))
                if track.album not in suggested_albums:
                    suggested_albums[track.album] = []
                suggested_albums[track.album].append('\t[{}] {}'.format(ind + 1, track.title))
        return suggested_albums

    def process_missing_albums(self, track_list, **kwargs):
        path_to_file = kwargs['path_to_file']
        missing_albums = self._find_missing_albums(track_list)
        if len(missing_albums) > 0:
            self._logger.warning('You may want to download this albums:')

            with codecs.open(path_to_file, 'w', 'utf-8') as f:
                for alb in sorted(missing_albums, key=lambda alb: len(missing_albums[alb]), reverse=True):
                    s = "[{}] {}".format(len(missing_albums[alb]), alb)
                    self._logger.warning(s)
                    f.write(s + '\n')
                    for track_name in missing_albums[alb]:
                        f.write(track_name + '\n')

    def _save_m3u(self, path_to_file: str, track_list: List[FileTrack], music_dir: str):
        path_to_file += '.m3u'
        self._logger.info("Saving m3u file: {}".format(path_to_file))
        with codecs.open(path_to_file, 'w', 'utf-8') as f:
            f.write(u'\ufeff#EXTM3U\n')
            for track in track_list:
                if track.is_found:
                    f.write(track.relative_filepath(music_dir) + "\n")
        self._logger.info("Saving completed")
