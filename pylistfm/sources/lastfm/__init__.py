import pylast
import requests
import logging
from uuid import UUID
from html.parser import HTMLParser
from pylistfm.sound_utils import Album


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False

    return True

class TrackParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tr = False
        self.current_track = {}
        self.tracks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'tr' and 'itemprop' in attrs and attrs['itemprop'] == 'track':
            self.in_tr = True
        elif self.in_tr and 'data-track-name' in attrs:
            self.current_track = {'track_name': attrs['data-track-name']}
        elif self.in_tr and tag == 'img' and 'alt' in attrs:
            self.current_track['album_name'] = attrs['alt']

    def handle_endtag(self, tag):
        if tag == 'tr' and self.in_tr:
            self.in_tr = False
            self.tracks.append(self.current_track)

class API:
    def __init__(self, config=None):
        self.network = pylast.LastFMNetwork(api_key=config['key'])
        self.source = config['source']
        self.date_preset = config['date_preset']

    def get_artist(self, artist_name):
        artist = None

        if validate_uuid4(artist_name):
            artist = self.network.get_artist_by_mbid(artist_name)
        else:
            request = self.network.search_for_artist(artist_name)
            artist = request.get_next_page()[0]

        logging.info('Found artist "{}"'.format(artist.name))
        return artist
    
    def get_tracks_by_api(self, artist, limit):
        results = []
        tracks = artist.get_top_tracks(limit)
        for track in tracks:
            album = track.item.get_album()
            try:
                results.append((track.item.title, album.title))
            except AttributeError:
                logging.warning('Cannot get album for track "{}"'.format(track.item.title))
                results.append((track.item.title, Album.NOT_FOUND))
        return results
    
    def get_tracks_by_html(self, artist, limit):
        results = []

        url = f'https://www.last.fm/music/{artist.name}/+tracks?date_preset={self.date_preset}'
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        parser = TrackParser()
        parser.feed(html_content)
        tracks = parser.tracks

        for track in tracks:
            try:
                results.append((track['track_name'], track['album_name']))
            except AttributeError:
                logging.warning('Cannot get album for track "{}"'.format(track.item.title))
                results.append((track['track_name'], Album.NOT_FOUND))
        return results[:limit]
        

    def get_top_tracks(self, artist_name, limit=10):
        results = []
        artist = self.get_artist(artist_name)

        if self.source == 'api':
            results = self.get_tracks_by_api(artist, limit)
        elif self.source == 'html':
            results = self.get_tracks_by_html(artist, limit)
        else:
            raise NotImplementedError('Unknown source')

        return results
