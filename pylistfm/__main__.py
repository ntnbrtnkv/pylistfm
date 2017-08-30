import argparse
import logging
import sys
from pylistfm.modes import string_to_mode
from pylistfm.config import Config
from pylistfm.playlist import Playlist


_config = None

def _main(playlist, artist):
    try:
        print('Start for {0}...'.format(artist))
        playlist.create_playlist(artist)
        print('\nComplete!')
    except KeyboardInterrupt:
        print("Quitting...")
        sys.exit(0)

def _parse_config_arg(arg_name, config, func=lambda x: x):
    atr = getattr(_args, arg_name)
    if atr is not None:
        setattr(config, arg_name, func(atr))


_parser = argparse.ArgumentParser(prog='python -m pylistfm')
_parser.add_argument('-m', '--mode', help='information to print', choices=['silent', 's', 'warning', 'w', 'information', 'i'])
_parser.add_argument('-i', '--init', help='initialize config.json', action='store_true')
_parser.add_argument('-l', '--limit', help='tracks limit', type=int)
_parser.add_argument('-d', '--dir', help='base dir to search')
_parser.add_argument('-a', '--artist', help='artist name')
_parser.add_argument('-s', '--search-missing-albums', help='search missing albums', action='store_true')

_args = _parser.parse_args()

if _args.init:
    _config = Config()
    _config.init()
    _config.save()
    sys.exit(0)

try:
    _config = Config()
    _config.load()
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

_parse_config_arg('mode', _config.pylistfm, func=string_to_mode)
try:
    _parse_config_arg('dir', _config.api['local']['dir'])
except KeyError as err:
    logging.warning(r'Trying to set local music dir when "local" module not configured')
_parse_config_arg('limit', _config.pylistfm)
_parse_config_arg('search_missing_albums', _config.pylistfm)

_main(Playlist(_config.pylistfm, _config.api), _artist)