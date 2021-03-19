from abc import abstractmethod
from typing import Union


class Title(str):
    pass


class Titleable:
    def __init__(self, title: Title = ''):
        self.title = title

    @property
    def title(self):
        return self._title

    def is_same_title(self, title: Title):
        return self.title.lower() == title.lower()

    @title.setter
    def title(self, value):
        self._title = value

    def __str__(self):
        return self.title


class Album(str):
    pass


class Track(Titleable):
    def __init__(self, title: Title = '', album: Album = None):
        super().__init__(title)
        self.album = album
        self._is_found = False

    @property
    def is_found(self):
        return self._is_found

    @is_found.setter
    def is_found(self, val):
        if not isinstance(val, bool):
            raise AttributeError
        self._is_found = val

    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, album: Union[Album, str]):
        if isinstance(album, Album):
            self._album = album
        elif isinstance(album, str):
            album_obj = Album(album)
            self._album = album_obj
        elif album is not None:
            raise AttributeError

    @property
    @abstractmethod
    def track(self):
        pass

    def __repr__(self):
        return f'{self.track} - {self.album}'

