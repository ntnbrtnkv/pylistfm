import os
import logging
from pathlib import Path
from datetime import date
import json
from uuid import UUID
from urllib import parse
import chardet


def detect_charset(filepath):
    with open(filepath, 'rb') as file:
        input_bytes = file.read()
        result = chardet.detect(input_bytes)
        return result['encoding'].lower()

def create_hardlink(path, base_dir, dest, index):
    filepath = '{}/{}'.format(base_dir, path)
    filename = os.path.basename(filepath)
    os.link(filepath, '{}/{:03d} - {}'.format(dest, index, filename))

def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False

    return True

def create_hardlist(source):
    _logger = logging.getLogger('pylistfm')
    _logger.info("Creating hardlist for playlist: {}".format(source))
    base_dir = os.path.dirname(source)
    source_basename = os.path.basename(source)
    source_filename = os.path.splitext(source_basename)[0]
    dest = '{}/{}'.format(base_dir, source_filename)
    _logger.info("Path for hardlist: {}".format(dest))
    if not os.path.exists(dest):
        _logger.warning("Path not found '{}', creating directories".format(dest))
        os.makedirs(dest)
    _logger.info("Creating hardlinks in destination path")
    charset = detect_charset(source)
    _logger.info("detected charset for '{}' as {}".format(source, charset))
    with open(source, 'r', encoding=charset) as playlist_file:
        tracks_files = filter(lambda line: line[0] != '#', list(playlist_file)[1:])
        for index, line in enumerate(tracks_files):
            path = line.rstrip('\n')
            try:
                create_hardlink(path, base_dir, dest, index)
            except FileNotFoundError:
                path = parse.unquote(path)
                create_hardlink(path, base_dir, dest, index)
    _logger.info("Hardlist has been created")

class CacheSource:
    def __init__(self, root):
        self._rootPath = Path(root)
        self._rootPath.mkdir(parents=True, exist_ok=True)
        self._datestring = date.today().strftime('%Y-%m-%d')

    def has(self, source, artist):
        return Path(self._rootPath, source, artist, self._datestring).exists()

    def save(self, source, artist, data):
        artistPath = Path(self._rootPath, source, artist)
        artistPath.mkdir(parents=True, exist_ok=True)
        filepath = artistPath / self._datestring
        with filepath.open(mode='w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def get(self, source, artist):
        result = None
        if (self.has(source, artist)):
            filepath = Path(self._rootPath, source, artist, self._datestring)
            with filepath.open(mode='r', encoding='utf-8') as f:
                result = json.load(f)
        return result