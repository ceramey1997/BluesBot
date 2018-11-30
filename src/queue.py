class SongQueue:

    def __init__(self):
        self.song_queue = []
    
    def add_song(self, song):
        self.song_queue.append(song)
    
    def add_album(self, album_list):
        for song in album_list:
            self.add_song(song)
    
    def add_playlist(self, playlist_list):
        for song in playlist_list:
            self.add_song(song)

    def remove_song(self, song):
        self.song_queue.remove(song)
    
    def pop_song(self, index=0):
        self.song_queue.pop(index)
    
    def length_queue(self):
        return len(self.song_queue)
    
    def get_song(self, index):
        return self.song_queue[index]
    
    def insert_song(self, index, song):
        self.song_queue.insert(index, song)
    
    def clear_queue(self):
        return self.song_queue.clear()
    
    def get_list(self):
        return self.song_queue