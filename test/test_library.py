import os
import json

import mock
import pytest

from blues_bot.src.library.library import Library

PATH = os.path.abspath('test/libraries.json')


EXPECTED = {
    'library': [{
        'name': 'new lib',
        'author': 'cole',
        'songs': ['taylor 22', 'mum & sons 40']
        }]
}


def _json_content():
    with open(PATH, 'r') as json_file:
        if json_file.readlines():
            json_file.seek(0)
        file_content = json.load(json_file)
    return file_content


# pylint: disable=R0904
class TestLibrary:

    @pytest.fixture
    def library(self):
        return Library(PATH)

    def setup(self):
        pass

    def teardown(self):
        if os.path.isfile(PATH):
            os.remove(PATH)

    def test_startup_make_file(self, library):
        if os.path.isfile(PATH):
            os.remove(PATH)
        library.startup_check()
        assert os.path.isfile(PATH)

    def test_startup_dont_make_file(self, library):
        library.startup_check()
        assert os.path.isfile(PATH)

    def test_save_libraries(self, library):
        library.add_library('new lib',
                            'cole',
                            ['taylor 22', 'mum & sons 40'])
        library.save_libraries()
        file_content = _json_content()
        assert EXPECTED == file_content

    def test_add_libraries(self, library):
        name = 'new lib'
        author = 'cole'
        songs = ['taylor 22', 'mum & sons 40']
        result = library.add_library(name, author, songs)
        file_content = _json_content()
        assert result == ('Library created',
                          'new lib library has been created by cole')
        assert EXPECTED == file_content

    def test_add_library_already_exists(self, library):
        name = 'new lib'
        author = 'cole'
        songs = ['taylor 22', 'mum & sons 40']
        library.add_library(name, author, songs)
        result = library.add_library(name, author, songs)
        assert result == ('Library already exists',
                          'Please use a different title')

    def test_add_library_no_songs(self, library):
        name = 'new lib'
        author = 'cole'
        library.add_library(name, author)
        file_content = _json_content()
        expected = {
            'library': [{
                'name': 'new lib',
                'author': 'cole',
                'songs': []
                }]
        }
        assert file_content == expected

    def test_delete_library(self, library):
        library.add_library('lib', 'cole')
        result = library.delete_library('lib')
        assert result == ('Library deleted',
                          'lib has been deleted')

    def test_delete_not_found(self, library):
        library.startup_check()
        result = library.delete_library('not real')
        assert result == ('Library could not be found',
                          'not real library does not exist')

    def test_show_libraries(self, library):
        name = ''
        library.add_library('lib', 'cole')
        library.add_library('next lib', 'grant')
        result = library.show_libraries(name)
        assert result == ('Here are all the existing libraries',
                          '\n1. lib (by cole)\n2. next lib (by grant)')

    def test_show_library_no_libs(self, library):
        name = ''
        result = library.show_libraries(name)
        assert result == ('There are no existing libraries',
                          'Use "!library create" to start a new library')

    def test_show_library_specific_lib(self, library):
        name = ' mylib'
        library.add_library('blahlib', 'steve', [])
        library.add_library('mylib', 'cole', ['mum 42', 'taylor 22'])
        result = library.show_libraries(name)
        expected = ('mylib (by cole)', '\n1. mum 42\n2. taylor 22')
        assert result == expected

    def test_show_library_specific_empty(self, library):
        name = ' mylib'
        library.add_library('mylib', 'cole')
        result = library.show_libraries(name)
        expected = ('mylib (by cole)', 'There are no songs in this library')
        assert result == expected

    def test_show_library_wrong_title(self, library):
        name = ' not real'
        result = library.show_libraries(name)
        assert result == ('The library could not be found', None)

    def test_set_library(self, library):
        lib_to_set = 'mylib'
        library.add_library('mylib', 'cole')
        result = library.set_library(lib_to_set)
        assert result == ('Library set',
                          'mylib is the current library',
                          mock.ANY)

    def test_set_library_fake_lib(self, library):
        lib = 'fakelib'
        library.add_library('mylib', 'cole')
        result = library.set_library(lib)
        assert result == ('Library not set',
                          'The library requested could not be found',
                          mock.ANY)

    def test_save_song(self, library):
        library.add_library('my new lib', 'cole')
        result = library.save_song('mum 42', 'my new lib')
        assert result == ('Song added',
                          'mum 42 was added to my new lib')

    def test_save_song_no_lib(self, library):
        result = library.save_song('mum 42', 'fake lib')
        assert result == (None,
                          'library does not exist')

    def test_save_song_song_already_there(self, library):
        library.add_library('my lib', 'cole', ['mum 42'])
        result = library.save_song('mum 42', 'my lib')
        assert result == ('Song already exists',
                          'Your song is already in my lib library')

    def test_remove_song(self, library):
        library.add_library('lib', 'cole', ['mum 42', 'yoyo'])
        result = library.remove_song('lib', 'mum 42')
        assert result == ('Song removed',
                          'mum 42 was removed from lib')

    def test_remove_song_no_song(self, library):
        library.add_library('lib', 'cole', ['mum 42', 'yoyo'])
        result = library.remove_song('lib', 'not a real song')
        assert result == ('Song not removed',
                          'Your library or song could not be found')

    def test_remove_song_fake_lib(self, library):
        library.add_library('lib', 'cole', ['mum 42', 'yoyo'])
        result = library.remove_song('fake lib', 'yoyo')
        assert result == ('Library does not exist', None)
