import spotipy
import os
import spotipy.util as Util

os.environ['SPOTIPY_CLIENT_ID'] = '6685f1fa024b4580b165fd845b74e8e4'
os.environ['SPOTIPY_CLIENT_SECRET'] = '02c2f1a11ef141898921ba58949bf41c'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://www.google.com/'

token = Util.prompt_for_user_token(username='jay101pk', scope='user-library-read')
sp = spotipy.Spotify(auth=token)  
results = sp.search(q='artist:coldplay', type='artist')
print(results)