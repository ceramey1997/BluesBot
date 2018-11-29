import json
import os

import spotipy
import spotipy.util as Util

__genres__ = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 
    'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 
    'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 
    'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 
    'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 
    'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 
    'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 
    'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 
    'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 
    'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 
    'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 
    'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 
    'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']

class SpotifyError(Exception):
    pass
class ArtistError(SpotifyError):
    pass
class AlbumError(SpotifyError):
    pass
class UserError(SpotifyError):
    pass
class PlaylistError(SpotifyError):
    pass


class bot_plugin(object):

    def __init__(self):
        f = open('creds.json','r')
        creds = json.loads(f.read())
        f.close()
        os.environ['SPOTIPY_CLIENT_ID'] = creds['SPOTIPY_CLIENT_ID']
        os.environ['SPOTIPY_CLIENT_SECRET'] = creds['SPOTIPY_CLIENT_SECRET']
        os.environ['SPOTIPY_REDIRECT_URI'] = creds['SPOTIPY_REDIRECT_URI']

        self.token = Util.prompt_for_user_token(username='jay101pk', scope='user-library-read')
        self.spotify = spotipy.Spotify(auth=self.token)
        
    def get_playlist(self, playlist, username=None):
        if username is None:
            username = self.spotify.current_user()['id']
        playlists = self.spotify.user_playlists(username)['items']
        for p in playlists:
            if p['name'] == playlist:
                break
        else:
            raise PlaylistError

        tracks_temp = self.spotify.user_playlist_tracks(username, p['id'])
        tracks_final= []
        for track in tracks_temp['items']:
            track = track['track']
            track_temp = ''
            for artist in track['artists']:
                track_temp += artist['name'] + ' '
            tracks_final.append(track_temp + track['name'])
        return tracks_final

    def get_album(self, album, artist):
        artists_list = self.spotify.search(artist,type='artist')['artists']['items']
        for art in artists_list:
            if art['name'].lower() == artist:
                break
        else:
            raise ArtistError
        
        albums_list = self.spotify.artist_albums(art['id'])
        for alb in albums_list['items']:
            if alb['name'].lower() == album:
                break
        else:
            raise AlbumError
        
        tracks_temp = self.spotify.album_tracks(alb['id'])
        tracks_final= []
        for track in tracks_temp['items']:
            track_temp = ''
            for artist in track['artists']:
                track_temp += artist['name'] + ' '
            tracks_final.append(track_temp + track['name'])
        return tracks_final

    def get_song_recs(self, songs=None, artists=None, genres=None, ):
        # TODO: add get recs
        pass

    def get_genres(self):
        return __genres__

    def get_user_playlists(self, username=None):
        if username is None:
            username = self.spotify.current_user()['id']
        
        playlists = self.spotify.user_playlists(username)['items']
        return [playlist['name'] for playlist in playlists]

    
