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
        mock_token.return_value = 'BQBtotZ1DKFd0t9DPd-ymyeSq7DJvpT55ezczmoDcFQC5vWyB9X6voXLQCnzQwphz8OHKOWwU07ee28qC0xjy5dxxul0Fquut4Q7ijD6jMm_2jnnKt-KkvvXDfpEAVb7CvDawl55nCIehWJMdR7Vl6dR7cE9Y-2DLNDvP-fspfeRp2zZpHc'
        spotify = SpotifyPlugin()
        spotify.spotify.search.return_value = search_value
        result = spotify._get_song_("Delta")

        assert result == 'Delta'

    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    def test_get_song_error(self, mock_spotify):
        spotify = SpotifyPlugin()
        spotify.spotify.search.return_value = {'tracks': {'items': [], 'is': 'are'}}

        with pytest.raises(spotify_exceptions.TrackError):
            spotify._get_song_("notASong")


    @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify')
    def test_get_artist(self, mock_spotify):
        search_value = {'artists': {'items': [{'id':
                                               'zeta'}],
                                    'is': 'are'}}

        spotify = SpotifyPlugin()
        spotify.spotify.search.return_value = search_value
        #mock_search.return_value = search_value
        result = spotify._get_artist_('zeta')

        assert result == 'zeta'

    # @mock.patch("blues_bot.spotify_plugin.spotipy.Spotify.search")
    # def test_get_artist_error(self, mock_search, spotify):
    #     mock_search.return_value = {'artists': {'items': [], 'is': 'are'}}
    #     with pytest.raises(spotify_exceptions.TrackError):
    #         spotify._get_artist_('fkArtist')

    #     mock_search.assert_called_once_with('fkArtist', type='artist')

    # def test_get_track_format(self, spotify):
    #     track = {'artists': [{'name': 'mum sons'}], 'name': '42'}
    #     return_value = spotify._get_track_format_(track)

    #     assert return_value == 'mum sons 42'

    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.user_playlist')
    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.next')
    # @mock.patch('blues_bot.spotify_plugin.SpotifyPlugin._get_track_format_')
    # def test_get_playlist_tracks(self, mock_track_format, mock_next,
    #                              mock_playlist, spotify):
    #     playlist = 'Coles Playlist'
    #     username = 'cr1997'
    #     mock_playlist.return_value = {'tracks': {'items': {
    #         'track': [{
    #             'mum sons': '2'}]},
    #                                              'name': '42'}}
    #     mock_next.return_value = []
    #     mock_track_format.return_value = 'mum and sons2'

    #     with pytest.raises(spotify_exceptions.PlaylistError):
    #         spotify.get_playlist_tracks(playlist, username)

    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.search')
    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.recommendations')
    # @mock.patch('blues_bot.spotify_plugin.SpotifyPlugin._get_track_format_')
    # def test_get_song_recommendations(self, mock_track_format, mock_recs, mock_search, spotify):
    #     mock_search.return_value = {'tracks': {'items': [{'id': 'the id'}]}}
    #     mock_recs.return_value = {'tracks': ['42', 'woman']}
    #     mock_track_format.return_value = 'song name'
    #     return_value = spotify.get_song_recommendations(songs=['42', 'woman'])
    #     expected_output = ['song name', 'song name']

    #     assert mock_track_format.call_count == 2
    #     mock_recs.assert_called_once_with(seed_artists=[],
    #                                       seed_genres=[],
    #                                       seed_tracks=['the id', 'the id'])
    #     assert mock_search.call_count == 2
    #     assert mock_track_format.call_count == 2
    #     assert return_value == expected_output

    # def test_get_genres(self, spotify):
    #     genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient',
    #               'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova',
    #               'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house',
    #               'children', 'chill', 'classical', 'club', 'comedy', 'country',
    #               'dance', 'dancehall', 'death-metal', 'deep-house',
    #               'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub',
    #               'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk',
    #               'forro', 'french', 'funk', 'garage', 'german', 'gospel',
    #               'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy',
    #               'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop',
    #               'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie',
    #               'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol',
    #               'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino',
    #               'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore',
    #               'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release',
    #               'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop',
    #               'pop-film', 'post-dubstep', 'power-pop', 'progressive-house',
    #               'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day',
    #               'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll',
    #               'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo',
    #               'show-tunes', 'singer-songwriter', 'ska', 'sleep',
    #               'songwriter', 'soul', 'soundtracks', 'spanish', 'study',
    #               'summer', 'swedish', 'synth-pop', 'tango', 'techno',
    #               'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
    #     result = spotify.get_genres()
    #     assert result == genres

    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.user_playlists')
    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.next')
    # def test_get_user_playlists(self, mock_next, mock_user_playlists, spotify):
    #     mock_next.return_value = []
    #     mock_user_playlists.return_value = {'items': [{'name': '1'}]}
    #     result = spotify.get_user_playlists()
    #     assert result == ['1']

    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.categories')
    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.next')
    # def test_get_categories(self, mock_next, mock_categories, spotify):
    #     cats = {'categories': {'items': [{'id': 'theid', 'name': 'thename'}]}}
    #     mock_categories.return_value = cats
    #     mock_next.return_value = []
    #     result = spotify.get_categories()
    #     assert result == ['theid']

    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.category_playlists')
    # @mock.patch('blues_bot.spotify_plugin.spotipy.Spotify.next')
    # def test_get_category_playlists(self, mock_next, mock_cat_list, spotify):
    #     mock_next.return_value = []
    #     mock_cat_list.return_value = {'playlists': {'items': [{'name': ['1']}]}}
    #     result = spotify.get_category_playlists('123456')

    #     mock_next.assert_called_once_with({'items': [{'name': ['1']}]})
    #     mock_cat_list.assert_called_once_with('123456')
    #     assert result == ['1']
