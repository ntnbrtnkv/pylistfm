import argparse
import logging
import sys
from pylistfm.modes import string_to_mode
from pylistfm.config import Config
from pylistfm.playlist import Playlist


_config = None


def _main(playlist, artist, output):
    try:
        print('Start for {0}...'.format(artist))
        playlist.create_playlist(artist, output)
        print('Complete!')
    except KeyboardInterrupt:
        print("Quitting...")
        sys.exit(0)


def _parse_config_arg(arg_name, config, setter=lambda x: x, success=None):
    atr = getattr(_args, arg_name)
    if atr is not None:
        val = setter(atr)
        setattr(config, arg_name, val)
        if callable(success):
            success(val)


_parser = argparse.ArgumentParser(prog='python -m pylistfm')
_parser.add_argument('-m', '--mode', help='information to print', choices=['silent', 's', 'warning', 'w', 'information', 'i'])
_parser.add_argument('-i', '--init', help='initialize config.json', action='store_true')
_parser.add_argument('-l', '--limit', help='tracks limit', type=int)
_parser.add_argument('--dir', help='base dir to search')
_parser.add_argument('-c', '--config', help='path to config', type=str)
_parser.add_argument('-a', '--artist', help='artist name or musicbrainz.org id')
_parser.add_argument('-o', '--output', help='alias for output dir', type=str)
_parser.add_argument('-d', '--debug', help='debug mode', action='store_true')
_parser.add_argument('-s', '--search-missing-albums', help='search missing albums', type=bool)

_args = _parser.parse_args()
logging.basicConfig()
_logger = logging.getLogger('pylistfm')

if _args.debug:
    _logger.setLevel(logging.DEBUG)

_logger.debug("Args %s", _args)

if _args.init:
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


if _args.artist is None:
    print('Artist name is required')
    _parser.print_usage()
    sys.exit(2)

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

_main(Playlist(_config.pylistfm, _config.api), _artist, _args.output)
