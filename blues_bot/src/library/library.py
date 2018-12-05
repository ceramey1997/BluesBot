"""Library class to manage local libraries"""
import io
import json
import os


class Library:
    """Handles user libraries

    Attributes:
        songs (list): library song list
        name (string): library name
        author (string): author name
    """

    path = 'blues_bot/src/library/libraries.json'

    def __init__(self, name, author, songs=None):
        if not songs:
            self.songs = []
        self.name = name
        self.author = author

    @staticmethod
    def startup_check():
        """Checks to see if library json file exists"""
        if not os.path.isfile(Library.path):
            with io.open(os.path.join(
                    'blues_bot/src/library/', 'libraries.json'), 'w') as json_file:
                json_file.write(json.dumps({"library": []}, indent=2))

    @staticmethod
    def save_libraries(data):
        """Saves libraries into json file

        Args:
            data (dict): json data to be saved
        """
        with open(Library.path, 'w') as outfile:
            json.dump(data, outfile, indent=2)

    @staticmethod
    def get_libraries():
        """Gets all libraries from json file

        Return:
                dict: dictionary of libraries
        """
        with open(Library.path, 'r') as json_file:
            if json_file.readlines():
                json_file.seek(0)
            return json.load(json_file)
