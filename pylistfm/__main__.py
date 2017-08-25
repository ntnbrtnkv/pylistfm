import getopt
import sys
from pylistfm.modes import Modes
from pylistfm.config import Config
from pylistfm.playlist import Playlist


def _main(playlist, artist):
    try:
        print('Start for {0}...'.format(artist))
        playlist.create_playlist(artist)
        print('\nComplete!')
    except KeyboardInterrupt:
        print("Quitting...")
        sys.exit(0)

help_string = """
Allowed options:
   -m, --mode <[s]ilent, [w]arning, [i]nformation>
   -a, --artist <artist_name>
   -s, --max-songs <count>
"""
artist = None
config = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:m:s:", ["artist=", "mode=", "max-songs="])
    config = Config()
except getopt.GetoptError as e:
    print(e)
    print(help_string)
    sys.exit(1)

if len(opts) > 0:
    for o, a in opts:
        # print("{} {}".format(o, a))
        if o in "-h":
            print(help_string)
            sys.exit()
        if o in ("-m", "--mode"):
            try:
                config.pylistfm.mode = Modes(a)
            except Exception:
                print(help_string)
                sys.exit(2)
        if o in ("-a", "--artist"):
            artist = a
        if o in ("-s", "--max-songs"):
            config.songsCount = int(a)

    playlist = Playlist(config.pylistfm, config.api)
    _main(playlist, artist)
else:
    print(help_string)