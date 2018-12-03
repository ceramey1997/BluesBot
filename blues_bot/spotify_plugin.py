"""Handles all Spotify interaction"""
# third-party
import json
import os
import spotipy
import spotipy.util as Util

# local
from blues_bot import spotify_exceptions


__genres__ = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient',
              'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova',
              'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house',
              'children', 'chill', 'classical', 'club', 'comedy', 'country',
              'dance', 'dancehall', 'death-metal', 'deep-house',
              'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub',
              'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk',
              'forro', 'french', 'funk', 'garage', 'german', 'gospel',
              'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy',
              'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop',
              'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie',
              'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol',
              'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino',
              'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore',
              'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release',
              'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop',
              'pop-film', 'post-dubstep', 'power-pop', 'progressive-house',
              'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day',
              'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll',
              'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo',
              'show-tunes', 'singer-songwriter', 'ska', 'sleep',
              'songwriter', 'soul', 'soundtracks', 'spanish', 'study',
              'summer', 'swedish', 'synth-pop', 'tango', 'techno',
              'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']


class SpotifyPlugin:
    """Spotify Object; handles all Spotify interactionqs"""
    def __init__(self):
        file_object = open('creds.json', 'r')
        creds = json.loads(file_object.read())
        file_object.close()
        os.environ['SPOTIPY_CLIENT_ID'] = creds['SPOTIPY_CLIENT_ID']
        os.environ['SPOTIPY_CLIENT_SECRET'] = creds['SPOTIPY_CLIENT_SECRET']
        os.environ['SPOTIPY_REDIRECT_URI'] = creds['SPOTIPY_REDIRECT_URI']

        token = Util.prompt_for_user_token(username='jay101pk',
                                           scope='user-library-read')
        self.spotify = spotipy.Spotify(auth=token)
        self.genres = self.spotify.recommendation_genre_seeds()['genres']

    def _get_song_(self, song_name):
        """Gets the song from spotify

        Args:
            song_name (Str): song to fine

        Raises:
            TrackError: if cannot find song you are looking for

        Returns:
            Str: song name you were searching for
        """
        results = self.spotify.search(song_name, type='track')
        results = results['tracks']['items']
        if not results:
            raise spotify_exceptions.TrackError('Track not found')
        return results[0]['id']

    def _get_artist_(self, artist_name):
        """Gets an artist from Spotify

        Args:
            artist_name (Str): artist to find

        Raises:
            TrackError: if cannot find artist you are looking for

        Returns:
            Str: artist name you were searching for
        """
        results = self.spotify.search(artist_name, type='artist')
        results = results['artists']['items']
        if not results:
            raise spotify_exceptions.TrackError('Track not found')
        return results[0]['id']

    @classmethod
    def _get_track_format_(cls, track):
        """Get the track format

        Args:
            track (Str): track to get format

        Returns:
            Str: track with correct formatting
        """
        track_temp = ''
        for artist in track['artists']:
            track_temp += artist['name'] + ' '
        return track_temp + track['name']

    def get_playlist_tracks(self, playlist, username='spotify'):
        """Get all playlist track from a given playlist

        Args:
            playlist (Str): name of playlist
            username (Str): defaults to spotify,
                            otherwise passed in
                            username of Spotify account

        Raises:
            PlaylistError: if cannot find the given playlist

        Returns:
            list: tracks from a playlist
        """
        playlists = self.spotify.user_playlists(username)['items']
        for p_list in playlists:
            if p_list['name'] == playlist:
                tracks_result = self.spotify.user_playlist(username,
                                                           p_list['id'])
                tracks_result = tracks_result['tracks']
                break
        else:
            raise spotify_exceptions.PlaylistError

        tracks_end = []
        while tracks_result:
            tracks_end.extend([SpotifyPlugin._get_track_format_(track['track'])
                               for track in tracks_result['items']])
            tracks_result = self.spotify.next(tracks_result)
        return tracks_end

    def get_album_tracks(self, album, artist):
        """Get all tracks from a given album

        Args:
            album (Str): album name to search
            artist (Str): artist name to search

        Raises:
            spotify_exceptions.AlbumError: if cannot find given album

        Returns:
            list: tracks from the given album
        """
        artist_results = self.spotify.search(artist,
                                             type='artist')
        artist_results = artist_results['artists']['items']
        if not artist_results:
            raise spotify_exceptions.ArtistError
        album_results = self.spotify.search(album + ' ' + artist, type='album')
        album_results = album_results['albums']['items']
        # for album in album_results['items']:
        #     for artist_found in artist_results:
        #         for artist in album['artists']:
        #             if artist['id'] == artist_found['id']:
        #                 break
        #         else:
        #             continue
        #         break
        #     else:
        #         continue
        #     break
        if album_results:
            album = album_results[0]
        else:
            raise spotify_exceptions.AlbumError
        # for artist_found in artist_results:
        #     album_results = self.spotify.search(album + ' ' +  artist,
        #                                         type='album')
        #     album_results = album_results['albums']
        #     for album in album_results['items']:
        #         for artist in album['artists']:
        #             if artist['id'] == artist_found['id']:
        #                 break
        #         else:
        #             continue
        #         break
        #     else:
        #         continue
        #     break
        # else:
        #     raise spotify_exceptions.AlbumError

        tracks_temp = self.spotify.album_tracks(album['id'])
        tracks_final = []
        for track in tracks_temp['items']:
            tracks_final.append(SpotifyPlugin._get_track_format_(track))
        return tracks_final

    def get_song_recommendations(self,
                                 songs=None,
                                 artists=None,
                                 genres=None):
        """Gets a list of 20 song recommendations

        Args:
            songs (list): list of songs to get recommendations off of
            artists (list): list of songs to get recommendations off of
            genres (list): list of songs to get recommendations off of

        Raises:
            AssertionError: if length of songs, artists, or genres
                            is longer than 5

        Returns:
            list: list of recommended songs
        """
        if not songs:
            songs = []
        if not artists:
            artists = []
        if not genres:
            genres = []
        if len(songs) + len(artists) + len(genres) > 5:
            error = 'Too many arguements passed in, must be 5 or less'
            raise AssertionError(error)

        song_ids = []
        for song in songs:
            song_ids.append(self._get_song_(song))

        artist_ids = []
        for artist in artists:
            artist_ids.append(self._get_artist_(artist))

        tracks = self.spotify.recommendations(seed_artists=artist_ids,
                                              seed_genres=genres,
                                              seed_tracks=song_ids)
        song_recs = []
        for track in tracks['tracks']:
            song_recs.append(SpotifyPlugin._get_track_format_(track))
        return song_recs

    def get_genres(self):
        """Gets all Genres

        Returns:
            list: list of all genres
        """
        return self.genres

    def get_user_playlists(self, username='spotify'):
        """Gets the users playlist

        Args:
            username (Str): username of Spotify user Defaults to spotify

        Returns:
            list: list of a users playlists
        """
        playlists = self.spotify.user_playlists(username, limit=50)
        playlist_list = []
        while playlists:
            playlist_list.extend(
                [playlist['name'] for playlist in playlists['items']])
            playlists = self.spotify.next(playlists)
        return playlist_list

    def get_categories(self):
        """Gets a list of categories from Spotify

        Returns:
            list: a list of category id's
        """
        category_list = []
        categories = self.spotify.categories()
        while categories:
            for cat in categories['categories']['items']:
                category_list.extend({cat['id']: cat['name']})
            categories = self.spotify.next(categories['categories'])
        return category_list

    def get_category_playlists(self, category_id):
        """Gets a list of playlists based off a category_id

        Args:
            category_id (Str): category id

        Returns:
            list: list of playlists based off of a category ID
        """
        playlist_list = []
        playlists = self.spotify.category_playlists(category_id)
        while playlists:
            for playlist in playlists['playlists']['items']:
                playlist_list.extend(playlist['name'])
            playlists = self.spotify.next(playlists['playlists'])
        return playlist_list

    def get_featured_playlists(self):
        """Gets Spotify featured playlists

        Returns:
            list: list of featured playlists
        """
        playlist_results = self.spotify.featured_playlists()['playlists']
        playlist_list = []
        while playlist_results:
            for playlist in playlist_results['items']:
                playlist_list.extend(playlist['name'])
            playlist_results = self.spotify.next(playlist_results)
        return playlist_list

    def refresh_token(self):
        """Refeshes the users Spotify token"""
        token = Util.prompt_for_user_token(username='jay101pk',
                                           scope='user-library-read')
        self.spotify = spotipy.Spotify(auth=token)
