import logging
import codecs
import glob
from .utils import Utils
from .sound_utils import TrackUtils, Track


class API:
    def __init__(self, glob_config, api_config):
        self._config = glob_config
        # logging.basicConfig(level=self._config.mode)
        self._dir = api_config['dir']
        self._types = api_config['types']
        self._playlist_type = api_config['playlist_type']

    def save(self, playlist_name, track_list, **kwargs):
        artist = kwargs['artist']
        config = self._config
        self._base_dir = self._dir + "/*" + ''.join(map(Utils.either, artist)) + "*/"
        music_dir = glob.glob(self._base_dir)[0]

        files_tracks = list(map(lambda tr: Track(tr), track_list))

        self._find_local_tracks(files_tracks)

        if config.search_missing_albums:
            self.process_missing_albums(files_tracks, path_to_file=music_dir + playlist_name + '_missing_albums')

        func = getattr(self, '_save_' + self._playlist_type)
        func(music_dir + playlist_name + '_pylistfm', files_tracks, music_dir)


    def _find_local_tracks(self, track_list):
        local_filepaths = []
        # Trying to find all files with given filetypes in base_dir with subdirs
        logging.info("Loading local music library")
        for _type in self._types:
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
                    if (not track.is_found or
                                track > file):
                        track.copy_fileinfo_from(file)
                    logging.info('Found song "{0}" in your collection'.format(track.title))

    def _find_missing_albums(self, track_list):
        suggested_albums = set('')
        for track in track_list:
            if not track.is_found:
                logging.warning('Not found song "{0} - {1}" in your collection\n'.format(track.title, track.album.title))
                if track.album is not None:
                    suggested_albums |= {track.album}
        return suggested_albums

    def process_missing_albums(self, track_list, **kwargs):
        path_to_file = kwargs['path_to_file']
        missing_albums = self._find_missing_albums(track_list)
        if len(missing_albums) > 0:
            logging.info('You may want to download this albums:')
            missing_albums = list(missing_albums)

            with codecs.open(path_to_file, 'w', 'utf-8') as f:
                for alb in missing_albums:
                    print("\"{}\"".format(alb))
                    f.write(alb.title + '\n')

    def _save_m3u(self, path_to_file, track_list, music_dir):
        path_to_file += '.m3u'
        logging.info("Saving m3u file: {}".format(path_to_file))
        with codecs.open(path_to_file, 'w', 'utf-8') as f:
            f.write(u'\ufeff#EXTM3U\n')
            for track in track_list:
                if track.is_found:
                    f.write(track.relative_filepath(music_dir) + "\n")
        logging.info("Saving completed")
