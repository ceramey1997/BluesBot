"""Library class to manage local libraries"""
import io
import json
import os
from random import shuffle


class Library:
    """Handles user libraries

    Attributes:
        songs (list): library song list
        name (string): library name
        author (string): author name
    """

    def __init__(self, path):
        self.path = path
        self.startup_check()
        self.libraries = self.get_libraries()

    def startup_check(self):
        """Checks to see if library json file exists"""
        if not os.path.isfile(self.path):
            with io.open(self.path, 'w') as json_file:
                json_file.write(json.dumps({"library": []}, indent=2))

    def save_libraries(self):
        """Saves libraries into json file

        Args:
            data (dict): json data to be saved
        """
        self.startup_check()
        with open(self.path, 'w') as outfile:
            json.dump(self.libraries, outfile, indent=2)

    def get_libraries(self):
        """Gets all libraries from json file

        Return:
                dict: dictionary of libraries
        """
        with open(self.path, 'r') as json_file:
            if json_file.readlines():
                json_file.seek(0)
            return json.load(json_file)

    def add_library(self, new_lib_name, author, songs=None):
        """Creates a user library.

        Args:
            new_lib_name (Str): string name for new library
            author (Str): string username of creator
            songs (list): list of songs to add to the library

        Return:
            (Str, Str): title and description for message
                to be sent in discord.
        """
        # check if the library exists
        if self._get_one_library(new_lib_name):
            title = 'Library already exists'
            description = 'Please use a different title'
            return (title, description)
        if not songs:
            songs = []
        data = {
            "name": new_lib_name,
            "author": author,
            "songs": songs
                }
        self.libraries['library'].append(data)
        self.save_libraries()
        title = "Library created"
        description = new_lib_name + ' library has been created by ' + author
        return (title, description)

    def delete_library(self, del_lib):
        """Deletes a given library

        Args:
            del_lib (Str): library to be deleted

        Return:
            (Str, Str): title and descption for discord message
        """
        gotten_lib = self._get_one_library(del_lib)
        if not gotten_lib:
            title = 'Library could not be found'
            description = del_lib + ' library does not exist'
        else:
            self.libraries['library'].remove(gotten_lib)
            self.save_libraries()
            title = 'Library deleted'
            description = del_lib + ' has been deleted'
        return (title, description)

    def show_libraries(self, name):
        """Show all libraries or specific library content

        Args:
            name (Str): name of library to show or none if just
                        want a list of all libraries

        Return:
            (Str, Str): title and description for discord message
        """
        title = None
        if name == '':
            title = 'Here are all the existing libraries'
            description = ''
            index = 1
            if not self.libraries['library']:
                title = 'There are no existing libraries'
                description = 'Use "!library create" to start a new library'
            for lib in self.libraries['library']:
                description += '\n' + str(index) + '. '
                description += lib['name'] + ' (by ' + lib['author'] + ')'
                index += 1
        else:
            name = name[1:]
            for library in self.libraries['library']:
                if library['name'] == name:
                    title = name + ' (by ' + library['author'] + ')'
                    description = ''
                    if not library['songs']:
                        description = 'There are no songs in this library'
                    else:
                        index = 1
                        for song in library['songs']:
                            description += '\n' + str(index) + '. ' + song
                            index += 1
        if not title:
            title = 'The library could not be found'
            description = None
        return (title, description)

    def set_library(self, lib_to_set):
        """Sets a library to be the playing library

        Args:
            lib_to_set (Str): the name of the library to set

        Return:
            (Str, Str, dict): title and description to send in discord
                              library to set.
        """
        set_library = self._get_one_library(lib_to_set)
        if not set_library:
            title = 'Library not set'
            description = 'The library requested could not be found'
            return (title, description, set_library)

        shuffle(set_library['songs'])
        title = 'Library set'
        description = set_library['name'] + ' is the current library'
        self.save_libraries()
        return (title, description, set_library)

    def save_song(self, song, library):
        """Save song to a Library

        Args:
            song (Str): name of the song to add to the library
            library_name (Str): name of the library to add a song to

        Return:
            (Str, Str): title and description for message sent in discord
        """
        library_edit = self._get_one_library(library)
        if not library_edit:
            title = None
            description = 'library does not exist'
        elif song not in library_edit['songs']:
            library_edit['songs'].append(song)
            title = 'Song added'
            description = song + ' was added to ' + library_edit['name']
        else:
            title = 'Song already exists'
            description = 'Your song is already in ' + library_edit['name'] + ' library'
        self.save_libraries()
        return (title, description)

    def remove_song(self, library_name, song_in):
        """Removes song from a library

        Arg:
            library_name (Str): name of the library to remove a song from
            song (Str): name of the song to remove

        Return:
            (Str, Str): title and description for message sent in discord
        """
        success = False
        song = ''
        library = self._get_one_library(library_name)
        if not library:
            title = 'Library does not exist'
            return (title, None)
        for song in library['songs']:
            if song_in.lower().strip() == song.lower().strip():
                library['songs'].remove(song)
                success = True
        if success:
            title = 'Song removed'
            description = song + ' was removed from ' + library['name']
        else:
            title = 'Song not removed'
            description = 'Your library or song could not be found'
        self.save_libraries()
        return (title, description)

    def _get_one_library(self, lib_name):
        """Gets a single library from library file

        Args:
            lib_name (Str): library name to get

        Return:
            (dict): single library if found, otherwise none
        """
        exists = None
        for lib in self.libraries['library']:
            if lib['name'] == lib_name:
                exists = lib
        return exists
