import io
import json
import os

class Library:
    path = 'blues_bot/src/library/libraries.json'

    def __init__(self, name, author, songs = []):
        self.songs = songs
        self.name = name
        self.author = author

    @staticmethod
    def startupCheck():
        if not os.path.isfile(Library.path):
            with io.open(os.path.join('src/library/', 'libraries.json'), 'w') as db_file:
                db_file.write(json.dumps({"library": []}, indent=2))

    def save_libraries(data):
        # add library structure to json
        # data = '{ name: "' + self.name + '", : ' + songs + ' }'
        # data = { "library": { "name": self.name, "songs": self.songs }} #Format!
        with open(Library.path, 'w') as outfile:
            json.dump(data, outfile, indent=2) 

    @staticmethod
    def get_libraries():
        with open(Library.path, 'r') as f:
            if len(f.readlines()) != 0:
                f.seek(0)
            return json.load(f)

    def add_song(self, song):
        self.songs.append(song)

