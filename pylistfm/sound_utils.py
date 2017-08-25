import os
from mutagen.easyid3 import EasyID3


class Titleable:
    def __init__(self, title=''):
        self._title = title
        self._lowered_title = title.lower()

    @property
    def title(self):
        return self._title

    @property
    def lowered_title(self):
        return self._lowered_title

    def __str__(self):
        return self.title


class Track(Titleable):
    def __init__(self, title='', album=None):
        super().__init__(title)
        self._id3_titles = None
        self._id3_lowered_titles = None
        self.album = album
        self._id3_info = None
        self._local_filepath = None
        self._lowered_filename = None

    def copy_fileinfo_from(self, source):
        if not isinstance(source, Track):
            raise AttributeError
        self.filepath = source.filepath
        self.id3_info = source.id3_info

    def found_at(self, filepath):
        self.filepath = filepath
        self.id3_info = EasyID3(filepath)

    def is_found_locally(self):
        return self._id3_titles is not None

    @property
    def lowered_filename(self):
        return self._lowered_filename

    def relative_filepath(self, base):
        n = len(base)
        return self._local_filepath[n:]

    @property
    def filepath(self):
        return self._local_filepath

    @filepath.setter
    def filepath(self, filepath):
        if not isinstance(filepath, str):
            raise AttributeError
        self._local_filepath = filepath
        self._lowered_filename = os.path.splitext(os.path.basename(filepath))[0].lower()

    @property
    def id3_info(self):
        return self._id3_info

    @id3_info.setter
    def id3_info(self, id3_info):
        if not isinstance(id3_info, EasyID3):
            raise AttributeError
        self._id3_info = id3_info
        self._id3_titles = self._id3_info['title']
        self._id3_lowered_titles = list(map(lambda x: x.lower(), self._id3_titles))

    @property
    def id3_lowered_titles(self):
        return self._id3_lowered_titles

    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, album):
        if isinstance(album, Album):
            self._album = album
        elif isinstance(album, str):
            album_obj = Album(album)
            self._album = album_obj
        elif album is not None:
            raise AttributeError

    def __gt__(self, other):
        if isinstance(other, Track):
            return (self.lowered_filename > other.lowered_filename or
                    self.id3_info.size > other.id3_info.size)
        else:
            raise NotImplementedError


class Album(Titleable):
    def __init__(self, title=''):
        super().__init__(title)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, Album):
            return self.title == other.title
        else:
            raise NotImplementedError


class TrackUtils:
    @staticmethod
    def _track_by_path(path):
        track = Track()
        track.found_at(path)
        return track

    @staticmethod
    def tracks_by_paths(paths):
        return list(map(lambda path: TrackUtils._track_by_path(path), paths))