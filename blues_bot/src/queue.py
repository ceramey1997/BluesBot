"""Handles all of the queue logic"""


class SongQueue:
    """handles Song Queue Logic and keep up with object

    Attributes:
        song_queue (list): song queue for blues bot
    """
    def __init__(self):
        self.song_queue = []

    def add_song(self, song):
        """Adds a song to the queue

        Args:
            song (Str): song to add to the queue
        """
        self.song_queue.append(song)

    def add_album(self, album_list):
        """Adds an album to the queue

        Args:
            album_list (list): album to add to the queue
        """
        for song in album_list:
            self.add_song(song)

    def add_playlist(self, playlist_list):
        """Adds a playlist to the queue

        Args:
            playlist_list (list): playlist to add to the queue
        """
        for song in playlist_list:
            self.add_song(song)

    def remove_song(self, song):
        """removes a song from the queue

        Args:
            song (Str): song to remove from the queue
        """
        self.song_queue.remove(song)

    def pop_song(self, index=0):
        """removes a song to the queue after it has been played

        Args:
            index (int): index of song to remove
        """
        self.song_queue.pop(index)

    def length_queue(self):
        """gets the current length of the song

        Returns:
            int: length of the queue
        """
        return len(self.song_queue)

    def get_song(self, index):
        """gets a single song at a specific index from the queue

        Args:
            index (int): index of queue of song to get

        Returns:
            Str: song name
        """
        return self.song_queue[index]

    def insert_song(self, index, song):
        """inserts a given song to the queue

        Args:
            index (int): place to put the new song
            song (Str): song name
        """
        self.song_queue.insert(index, song)

    def clear_queue(self):
        """Resets Queue with no songs on it

        Returns:
            list: empty song_queue
        """
        return self.song_queue.clear()

    def get_list(self):
        """gets the song queue

        Returns:
            list: current song queue
        """
        return self.song_queue
