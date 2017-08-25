import pylast


class API:
    def __init__(self, config=None):
        self.network = pylast.LastFMNetwork(api_key=config['key'])

    def get_top_tracks(self, artist_name, limit=10):
        results = []
        request = self.network.search_for_artist(artist_name)
        artist = request.get_next_page()[0]
        tracks = artist.get_top_tracks(limit)
        for track in tracks:
            album = track.item.get_album()
            results.append((track.item.title, album.title))
        return results
