import spotipy
import os
import spotipy.util as Util
class bot_plugin(object):

    def __init__(self):
        os.environ['SPOTIPY_CLIENT_ID'] = '6685f1fa024b4580b165fd845b74e8e4'
        os.environ['SPOTIPY_CLIENT_SECRET'] = '02c2f1a11ef141898921ba58949bf41c'
        os.environ['SPOTIPY_REDIRECT_URI'] = 'https://www.google.com/'

        self.token = Util.prompt_for_user_token(username='jay101pk', scope='user-library-read')
        self.spotify = spotipy.Spotify(auth=self.token)
        

    def get_playlist(self, playlist, username=None):
        if username is None:
            username = self.spotify.current_user()['id']
        
        playlists = self.spotify.user_playlists(username)['items']
        for p in playlists:
            if p == playlist:
                break
        tracks_temp = self.spotify.user_playlist_tracks(username, p['id'])
        tracks_final= []
        for track in tracks_temp['items']:
            track = track['track']
            track_temp = ''
            for artist in track['artists']:
                track_temp += artist['name'] + ' '
            tracks_final.append(track_temp + track['name'])
        return tracks_final

    
        



# print(results.keys())
bot = bot_plugin()
sp = bot.spotify

print(bot.get_playlist('My Shazam Tracks','jay101pk'))
        