"""Spotify Exceptions"""


class SpotifyError(Exception):
    """General Spotify Error"""


class ArtistError(SpotifyError):
    """Spotify Artist Error"""


class AlbumError(SpotifyError):
    """Spotify Album Error"""


class UserError(SpotifyError):
    """Spotify User Error"""


class PlaylistError(SpotifyError):
    """Spotify Playlist Error"""


class TrackError(SpotifyError):
    """Spotify Track Error"""
