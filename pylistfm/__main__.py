import argparse
import logging
import sys
import os
from pylistfm.modes import string_to_mode
from pylistfm.config import Config, default_filename
from pylistfm.playlist import Playlist
from pylistfm.utils import create_hardlist


_config = None


def _main(playlist, artist, output, mbid):
    try:
        print('Start for {0}...'.format(artist))
        playlist.create_playlist(artist, output, mbid)
        print('Complete!')
    except KeyboardInterrupt:
        print("Quitting...")
        sys.exit(0)


def _parse_config_arg(arg_name, config, config_attr_name=None, setter=lambda x: x, success=None):
    atr = getattr(_args, arg_name)
    if atr is not None:
        val = setter(atr)
        setattr(config, arg_name if config_attr_name is None else config_attr_name, val)
        if callable(success):
            success(val)


_parser = argparse.ArgumentParser(prog='python -m pylistfm')
_parser.add_argument('-m', '--mode', help='information to print', choices=['silent', 's', 'warning', 'w', 'information', 'i'])
_parser.add_argument('-i', '--init', help='initialize config.json', action='store_true')
_parser.add_argument('-l', '--limit', help='tracks limit', type=int)
_parser.add_argument('--dir', help='base dir to search')
_parser.add_argument('--disable-cache', help='disable cache, false by default', action='store_true')
_parser.add_argument('-c', '--config', help='path to config', type=str)
_parser.add_argument('-a', '--artist', help='artist name')
_parser.add_argument('--mbid', help='musicbrainz.org id')
_parser.add_argument('-o', '--output', help='alias for output dir', type=str)
_parser.add_argument('-d', '--debug', help='debug mode', action='store_true')
_parser.add_argument('-s', '--search-missing-albums', help='search missing albums', type=bool)
_parser.add_argument('-p', '--copy-playlist', help='create hardlist by path to m3u file', type=str)

_args = _parser.parse_args()
logging.basicConfig()
_logger = logging.getLogger('pylistfm')

if _args.debug:
    _logger.setLevel(logging.DEBUG)

_logger.debug("Args %s", _args)

if _args.init:
    if os.path.isfile(default_filename):
        _logger.error("File\" %s\" already exists. Delete it before reinitializing.", default_filename)
        sys.exit(1)
    _config = Config()
    _config.init()
    _config.save()
    sys.exit(0)

try:
    _config = Config()
    _config.load()
    _logger.debug("Loaded config from \"%s\": %s", _config.filename, _config)
except FileNotFoundError:
    print("""
Please initialize config
""")
    _parser.print_help()
    sys.exit(1)

if _args.copy_playlist is not None:
    create_hardlist(_args.copy_playlist)
    sys.exit(0)

if _args.artist is None:
    print('Artist name is required')
    _parser.print_usage()
    sys.exit(2)

if _args.disable_cache:
    _parse_config_arg('disable_cache', _config.pylistfm, config_attr_name='cache', setter=lambda _: None)

_artist = _args.artist

if _args.mode is None:
    _logger.setLevel(_config.pylistfm.mode)
else:
    _parse_config_arg('mode', _config.pylistfm, setter=string_to_mode, success=lambda val: _logger.setLevel(val) if _logger.level != logging.DEBUG else val)
try:
    _parse_config_arg('dir', _config.api['local']['dir'])
except KeyError as err:
    logging.warning(r'Trying to set local music dir when "local" module not configured')
_parse_config_arg('limit', _config.pylistfm)
_parse_config_arg('search_missing_albums', _config.pylistfm)

_logger.debug("After args: %s", _config)

_main(Playlist(_config.pylistfm, _config.api), _artist, _args.output, _args.mbid)
