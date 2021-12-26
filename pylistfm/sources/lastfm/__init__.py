import pylast
import logging
from uuid import UUID
from pylistfm.sound_utils import Album


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False

    return True

class API:
    def __init__(self, config=None):
        self.network = pylast.LastFMNetwork(api_key=config['key'])

    def get_top_tracks(self, artist_name, limit=10):
        results = []
        artist = None

        if validate_uuid4(artist_name):
            artist = self.network.get_artist_by_mbid(artist_name)
        else:
            request = self.network.search_for_artist(artist_name)
            artist = request.get_next_page()[0]

        logging.info('Found artist "{}"'.format(artist.name))

        tracks = artist.get_top_tracks(limit)
        for track in tracks:
            album = track.item.get_album()
            try:
                results.append((track.item.title, album.title))
            except AttributeError:
                logging.warning('Cannot get album for track "{}"'.format(track.item.title))
                results.append((track.item.title, Album.NOT_FOUND))
        return results
