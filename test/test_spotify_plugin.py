"""Test's Spotify Plugin File"""
import pytest
import mock
from blues_bot.spotify_plugin import SpotifyPlugin
from blues_bot import spotify_exceptions


class TestSpotifyPlugin:

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_song(self, mock_token, mock_spotipy):
        search_value = {'tracks': {'items': [{'id':
                                              'Delta'}],
                                   'is': 'are'}}
        spotify = SpotifyPlugin()
        mock_token.return_value = 'BQBtotZ1'
        spotify.spotify.search.return_value = search_value
        result = spotify._get_song_("Delta")

        assert result == 'Delta'

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_song_error(self, mock_token, mock_spotify):
        mock_token.return_value = 'BQBtotZ1'
        spotify = SpotifyPlugin()
        spotify.spotify.search.return_value = {'tracks': {'items': [], 'is': 'are'}}

        with pytest.raises(spotify_exceptions.TrackError):
            spotify._get_song_("notASong")

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_artist(self, mock_token, mock_spotify):
        search_value = {'artists': {'items': [{'id':
                                               'zeta'}],
                                    'is': 'are'}}
        mock_token.return_value = 'BQBtotZ1'
        spotify = SpotifyPlugin()
        spotify.spotify.search.return_value = search_value
        result = spotify._get_artist_('zeta')

        assert result == 'zeta'

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_artist_error(self, mock_token, mock_spotify):
        mock_token = 'BQBtotZ1'
        spotify = SpotifyPlugin()
        spotify.spotify.search.return_value = {'artists': {'items': [], 'is': 'are'}}
        with pytest.raises(spotify_exceptions.TrackError):
            spotify._get_artist_('fkArtist')

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_track_format(self, mock_token, mock_spotify):
        spotify = SpotifyPlugin()
        mock_token.return_value = 'BQBtotZ1'
        track = {'artists': [{'name': 'mum sons'}], 'name': '42'}
        return_value = spotify._get_track_format_(track)

        assert return_value == 'mum sons 42'

    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.user_playlist')
    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.SpotifyPlugin._get_track_format_')
    def test_get_playlist_tracks(self, mock_track_format, mock_spotify,
                                 mock_playlist, mock_token):
        mock_token.return_value = 'BQBtotZ1'
        spotify = SpotifyPlugin()

        playlist = 'Coles Playlist'
        username = 'cr1997'
        mock_playlist.return_value = {'tracks': {'items': {
            'track': [{
                'mum sons': '2'}]},
                                                 'name': '42'}}
        spotify.spotify.next.return_value = []
        mock_track_format.return_value = 'mum and sons2'

        with pytest.raises(spotify_exceptions.PlaylistError):
            spotify.get_playlist_tracks(playlist, username)

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.SpotifyPlugin._get_track_format_')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_song_recommendations(self, mock_token, mock_track_format, mock_spotify):
        mock_token.return_value = 'the_fake_token'
        spotify = SpotifyPlugin()
        spotify.spotify.search.return_value = {'tracks': {'items': [{'id': 'the id'}]}}
        spotify.spotify.recommendations.return_value = {'tracks': ['42', 'woman']}
        mock_track_format.return_value = 'song name'
        return_value = spotify.get_song_recommendations(songs=['42', 'woman'])
        expected_output = ['song name', 'song name']

        assert mock_track_format.call_count == 2
        assert mock_track_format.call_count == 2
        assert return_value == expected_output

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_user_playlists(self, mock_token, mock_spotify):
        mock_token = 'the_fake_token'
        spotify = SpotifyPlugin()
        spotify.spotify.next.return_value = []
        spotify.spotify.user_playlists.return_value = {'items': [{'name': '1'}]}
        result = spotify.get_user_playlists()

        assert result == ['1']

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.categories')
    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_categories(self, mock_token, mock_spotify, mock_categories):
        mock_token = 'the_fake_token'
        spotify = SpotifyPlugin()
        cats = {'categories': {'items': [{'id': 'theid', 'name': 'thename'}]}}
        spotify.spotify.categories.return_value = cats
        spotify.spotify.next.return_value = []
        result = spotify.get_categories()
        assert result == ['theid']

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    @mock.patch('blues_bot.spotify_plugin.spotipy.util.prompt_for_user_token')
    def test_get_category_playlists(self, mock_token, mock_spotify):
        mock_token = 'the_fake_token'
        spotify = SpotifyPlugin()
        spotify.spotify.next.return_value = []
        cats = {'playlists': {'items': [{'name': ['1']}]}}
        spotify.spotify.category_playlists.return_value = cats
        result = spotify.get_category_playlists('123456')

        assert result == ['1']
