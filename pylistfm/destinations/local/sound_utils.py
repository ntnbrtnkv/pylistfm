import os
from typing import List, Optional, TypedDict, cast
from mutagen import File, flac, mp3
from pylistfm.sound_utils import Track as DefaultTrack, Title, Album


class TagsInfo(TypedDict):
    album: List[str]
    title: List[str]


class Tags:
    albums: List[Album] = []
    titles: List[Title] = []


class InfoBlock(TypedDict):
    bitrate: int


class Track(DefaultTrack):
    def __init__(self, track: 'Track' = None):
        if track is None:
            super().__init__()
        else:
            super().__init__(track.title, track.album)
        self._local_filepath: Optional[str] = None
        self._lowered_filename: Optional[str] = None
        self._tags = Tags()
        self._bitrate: int = 0
        self._filesize: int = 0

    def load_from_filepath(self, filepath: str):
        self.filepath = filepath
        self._filesize = os.stat(filepath).st_size
        file = File(filepath)
        mime = file.mime
        tags: Optional[TagsInfo] = None
        info: InfoBlock = InfoBlock()
        if 'audio/mp3' in mime:
            mp3_data = mp3.EasyMP3(filepath)
            tags = cast(TagsInfo, mp3_data)
            info = cast(InfoBlock, mp3_data.info)
        elif 'audio/flac' in mime:
            flac_data = flac.FLAC(filepath)
            tags = cast(TagsInfo, flac_data)
            info = cast(InfoBlock, flac_data.info)
        else:
            raise TypeError
        self._bitrate = info.bitrate
        self._tags.titles = tags['title']
        self._tags.albums = tags['album']
        self.is_found = True

    def is_title_same(self, title: Title) -> bool:
        lowered_title = title.lower()
        return lowered_title in self._tags.titles

    def copy_info_from(self, source: 'Track'):
        if not isinstance(source, Track):
            raise AttributeError
        self.filepath = source.filepath
        self.is_found = source.is_found

    @property
    def filesize(self) -> int:
        return self._filesize

    @property
    def filepath(self):
        return self._local_filepath

    @filepath.setter
    def filepath(self, filepath: str):
        if not isinstance(filepath, str):
            raise AttributeError
        self._local_filepath = filepath
        self._lowered_filename = os.path.splitext(os.path.basename(filepath))[0].lower()

    @property
    def bitrate(self):
        return self._bitrate

    @property
    def lowered_filename(self) -> str:
        return self._lowered_filename

    def relative_filepath(self, base: str):
        n = len(base)
        # Make more safe
        return self._local_filepath[n:]

    def __gt__(self, other: 'Track'):
        if isinstance(other, Track):
            return (self.bitrate > other.bitrate or
                    self.lowered_filename > other.lowered_filename or
                    self.filesize > other.filesize)
        else:
            raise NotImplementedError


class TrackUtils:
    @staticmethod
    def _track_by_path(path):
        track = Track()
        track.load_from_filepath(path)
        return track

    @staticmethod
    def tracks_by_paths(paths):
        return list(map(lambda path: TrackUtils._track_by_path(path), paths))
