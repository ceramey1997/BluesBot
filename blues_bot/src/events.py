"""event class that handles all discord events"""
# python packages
import asyncio
import logging

# third party
from spotipy.client import SpotifyException
import discord

# local
from blues_bot.src.users.user import User
from blues_bot.src.search_engine import search_yt
from blues_bot.src.stop_sign import StopSign
from blues_bot.spotify_plugin import SpotifyPlugin
from blues_bot import spotify_exceptions
from blues_bot.src.library.library import Library


# pylint: disable=R0904, R0902
class EventMessage:
    """Handles user input.

    Attributes:
        song_queue (SongQueue): song_queue object, a list of songs in queue
        stopper (StopSign): StopSign object for if song is playing or not
        song_queue (list): song queue list
        first_flag (bool): stops it from playing if song is already playing
        users (dictionary): users with history
        sp_ob (SpotifyPlugin): SpotifyPlugin Object to handle spotify stuff
    """
    def __init__(self, song_queue):
        self.log = logging.getLogger()
        self.stopper = StopSign(False)
        self.song_queue = song_queue
        self.first_flag = False
        self.users = {}
        self.sp_ob = SpotifyPlugin()
        self.libraries = Library('blues_bot/src/library/libraries.json')
        self.current_library = None

    # pylint: disable=R0912, R0915
    async def message_recieved(self, client, message):
        """top level recieve message function that
           handles all incoming message.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        if message.author.name not in self.users:
            user_in = User(message.author)
            self.users[message.author.name] = user_in

        if message.content.startswith('!hello'):
            await self.message_hello(client, message)
        tries = 0
        while tries < 3:
            try:
                if message.content.startswith('!play'):
                    channel = message.channel
                    if message.content.startswith('!play album'):
                        await self.message_play_album(client,
                                                      message,
                                                      channel)
                    elif message.content.startswith('!play playlist'):
                        await self.message_play_playlist(client,
                                                         message,
                                                         channel)
                    else:
                        msg = message.content.replace('!play ', '')
                        self.song_queue.add_song(msg)
                        self.users[message.author.name].history.insert(0, msg)
                        if self.song_queue.length_queue() == 1:
                            await self.message_play_song(client, msg, message)
                break
            except SpotifyException:
                self.sp_ob.refresh_token()
                tries += 1
        assert tries < 3, 'Could not get token'

        if message.content.startswith('!queue'):
            await self.message_queue(client, message)

        elif message.content.startswith('!history'):
            await self.message_history(client, message)
        elif message.content.startswith('!join'):
            await self._join(client, message)

        elif message.content.startswith('!help'):
            await self.help(client, message)

        elif message.content.startswith('!skip'):
            await self.message_skip(client)

        elif message.content.startswith('!remove'):
            song = message.content.replace('!remove ', '')
            await self.remove_song(client, message, song)

        elif message.content.startswith('!remove'):
            song = message.content.replace('!remove ', '')
            await self.remove_song(client, message, song)

        elif message.content.startswith('!repeat'):
            await self.message_repeat(client, message)

        elif message.content.startswith('!rec'):
            if message.content.startswith('!rec get'):
                await self.get_recommendations(client, message)
            elif message.content.startswith('!rec add'):
                await self.add_recommendations(client, message)

        elif message.content.startswith('!quit'):
            await self.message_quit(client)

        elif message.content.startswith('!restart'):
            await self.message_restart(client)

        elif message.content.startswith('!library'):
            self.libraries.startup_check()
            if message.content.startswith('!library create'):
                await self.message_create_library(client, message)

            elif message.content.startswith('!library show'):
                await self.message_show_libraries(client, message)

            elif message.content.startswith('!library set'):
                await self.message_set_library(client, message)

            elif message.content.startswith('!library current'):
                await self.message_current_library(client, message)

            elif message.content.startswith('!library save'):
                await self.message_library_save_song(client, message)

            elif message.content.startswith('!library remove'):
                await self.message_library_remove_song(client, message)

            elif message.content.startswith('!library delete'):
                await self.message_delete_library(client, message)

    async def message_hello(self, client, message):
        """Messages an in chat hello message.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        msg = 'Hello ' + message.author.name
        # wait self.create_embed(client, message, None, msg, True)
        await client.send_message(message.channel, msg, tts=True)

    async def _goodbye(self, client, message):
        """Messages in chat goodbye before bot leaves channel

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        msg = 'Later nerds!'
        await client.send_message(message.channel, msg, tts=True)

    async def message_play_album(self, client, message, channel):
        """Takes the input of an album and plays if first thing
           in queue otherwise adds to back of queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
            channel (Str): Chat channel that the user sent the message from
        """
        msg = message.content.replace('!play album ', '')
        album, artist = msg.split(",")
        album = album.strip()
        artist = artist.strip()
        description = ''
        try:
            album_info = self.sp_ob.get_album_tracks(album, artist)
        except spotify_exceptions.SpotifyError as spot_error:
            if isinstance(spot_error, spotify_exceptions.AlbumError):
                msg = 'Invalid album name'
            elif isinstance(spot_error, spotify_exceptions.ArtistError):
                msg = 'Invalid artist name'
            else:
                self.log.error(str(spot_error))
                print(spot_error.args)
                return
            await client.send_message(channel, msg)
            return
        for song in album_info:
            self.song_queue.add_song(song)
            self.users[message.author.name].history.insert(0, song)
            description += "\n" + song
            if self.song_queue.length_queue() == 1:
                self.first_flag = True

        title = "Songs Added To Queue:\n\tAlbum: "
        title += album + "\n\tArtist: " + artist
        await self._create_embed(client, message,
                                 title, description)

        if self.first_flag:
            await self.message_play_song(client,
                                         self.song_queue.get_song(0),
                                         message)

    async def message_play_playlist(self, client, message, channel):
        """Takes the input of an playlist and plays if first thing
           in queue otherwise adds to back of queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
            channel (Str): Chat channel that the user sent the message from
        """
        msg = message.content.replace('!play playlist ', '')
        playlist, username = msg.split(',')
        playlist = playlist.strip()
        username = username.strip()
        description = ''
        try:
            playlist_info = (
                self.sp_ob.get_playlist_tracks(playlist,
                                               username))
        except spotify_exceptions.SpotifyError as spot_error:
            if isinstance(spot_error, spotify_exceptions.PlaylistError):
                msg = 'Invalid playlist name'
            elif isinstance(spot_error, spotify_exceptions.UserError):
                msg = 'Invalid username'
            else:
                self.log.error(str(spot_error))
                print(spot_error.args)
                return
            await client.send_message(channel, msg)
            return
        for song in playlist_info:
            self.song_queue.add_song(song)
            self.users[message.author.name].history.insert(0, song)
            description += '\n' + song
            if self.song_queue.length_queue() == 1:
                self.first_flag = True

        title = "Songs Added To Queue From:\n\t" + playlist
        await self._create_embed(client, message,
                                 title, description)

        if self.first_flag:
            await self.message_play_song(client,
                                         self.song_queue.get_song(0),
                                         message)

    async def message_queue(self, client, message):
        """Sends a message of what is on the current Queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        index = 1
        title = 'The current song queue is:'
        msg = ''
        for song in self.song_queue.get_list():
            msg += '\n ' + str(index) + '. ' + song
            index += 1

        await self._create_embed(client, message, title, msg)

    async def message_history(self, client, message):
        """Sends a message in chat channel of the user's last 10 adds
           to the queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        username = ''
        title = 'Here are the last 10 songs requested by '

        msg = message.content.strip().lower() == '!history '
        if message.content.strip().lower() == '!history':
            username = message.author.name
        else:
            for key in self.users:
                if msg == key:
                    username = key

        if not username:
            await client.send_message(message.channel,
                                      'That user does not exist')
            return
        title += username
        history = self.users[username].history
        msg = ''
        index = 0
        while index < 10:
            if index >= len(history):
                break
            msg += '\n ' + str(index + 1) + '. ' + history[index]
            index += 1
        await self._create_embed(client, message, title, msg)

    async def _join(self, client, message):
        """joins a voice channel.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        server_id = message.author.server.id
        if not client.is_voice_connected(client.get_server(server_id)):
            voice_channel = message.author.voice.voice_channel
            if not voice_channel:
                title = "you don't seem to be in the channel"
                await self._create_embed(client, message, title=title)
                return None
            voice_client = await client.join_voice_channel(voice_channel)
        voice_client = client.voice_client_in(client.get_server(server_id))
        return voice_client

    async def message_play_song(self, client, query, message):
        """Takes a song and query's youtube and joins the server
           if necessary, and plays the song.

        Args:
            client (Client): client object from Discord
            query (Str): song name and artist to query youtube with
            message (Message): message object from Discord
        """
        self.first_flag = False
        voice_client = await self._join(client, message)
        if voice_client is None:
            return
        url = search_yt(query)
        player = await voice_client.create_ytdl_player(url)
        player.volume = 0.4  # 0.25
        player.start()
        await self._change_status(client, query)

        # pylint: disable=W0612
        for i in range(int(player.duration)):
            await asyncio.sleep(1)
            if self.stopper.get_flag():
                player.stop()
                self.stopper.set_flag(False)
                break
        self.song_queue.pop_song()
        if self.song_queue.length_queue() > 0:
            await self.message_play_song(client,
                                         self.song_queue.get_song(0),
                                         message)
        else:
            await self._goodbye(client, message)
            await voice_client.disconnect()
            self.first_flag = False
            await self._change_status(client, None)

    async def _change_status(self, client, song_name):
        """Changes the status of the bot
            (on the far right of discord where it shows
            what game user's are playing)

        Args:
            client (Client): client object from Discord
            song_name (Str): song name to play
        """
        await client.change_presence(game=discord.Game(name=song_name))

    async def message_repeat(self, client, message):
        """Put's the song that is playing again at the top
           of the Queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        current_song = self.song_queue.get_song(0)
        self.song_queue.insert_song(1, current_song)
        msg = current_song + ' will be repeated'
        await client.send_message(message.channel, msg)

    async def _create_embed(self, client, message,
                            title=None, description=None):
        """Creates a pretty embed message and send the message.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
            title (Str): title to add as embed object
            description (Str): Description box of embed object

        """
        embed = discord.Embed(title=title,
                              description=description,
                              colour=0xDEADBF)
        await client.send_message(message.channel, embed=embed)

    async def message_skip(self, client):
        """Skips the current song that is playing.

        Args:
            client (Client): client object from Discord
        """
        await self._change_status(client, None)
        self.stopper.set_flag(True)

    async def remove_song(self, client, message, song_name):
        """Removes a given song from the queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
            song_name (Str): song name to remove from the queue
        """
        for song in self.song_queue.get_list():
            if song_name.lower() in song.lower():
                self.song_queue.remove_song(song)
                msg = song + " has been removed from the queue"
                await self._create_embed(client, message, title=msg)
                return
        msg = song_name + " is not found in the queue"
        await self._create_embed(client, message, title=msg)

    async def get_recommendations(self, client, message):
        """Gets the recommendations for a user from Spotify
           based on (at most) the previous 5 songs added to the
           queue and prints them in an embed message.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        person = self.users[message.author.name]
        # pep8 --ignore=E501
        recs = self.sp_ob.get_song_recommendations(songs=[person.history[:5]])
        msg = ''
        person.recommendations = recs
        for line in recs:
            msg += line + '\n'
        title = 'Songs recommended to you ' + message.author.name
        await self._create_embed(client, message,
                                 title=title, description=msg)

    async def add_recommendations(self, client, message):
        """Takes the songs from get_recommendations and adds them
           to the queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        person = self.users[message.author.name]
        try:
            recs = person.recommendations
        except AttributeError:
            await self.get_recommendations(client, message)
            recs = person.recommendations
        description = ''
        for song in recs:
            self.song_queue.add_song(song)
            self.users[message.author.name].history.insert(0, song)
            description += '\n' + song
            if self.song_queue.length_queue() == 1:
                self.first_flag = True
        title = "Songs Added To Queue From:\n\tRecommendations"
        await self._create_embed(client, message, title, description)

        if self.first_flag:
            await self.message_play_song(client,
                                         self.song_queue.get_song(0),
                                         message)

    async def message_create_library(self, client, message):
        """Creates a user library.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        name = message.content.replace('!library create ', '')
        # check if the library exists
        title, description = self.libraries.add_library(name, message.author.name)
        await self._create_embed(client, message, title, description)

    async def message_delete_library(self, client, message):
        """Deletes a user library.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        name = message.content.replace('!library delete ', '')
        title, description = self.libraries.delete_library(name)
        await self._create_embed(client, message, title, description)

    async def message_show_libraries(self, client, message):
        """Shows a certain library's info or all libraries if not specified.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        name = message.content.replace('!library show', '')
        title, description = self.libraries.show_libraries(name)
        await self._create_embed(client, message, title, description)

    async def message_set_library(self, client, message):
        """Sets a library to be used when no requests are given.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """

        name = message.content.replace('!library set ', '')
        title, description, set_library = self.libraries.set_library(name)
        self.current_library = set_library

        await self._create_embed(client, message, title, description)

    async def message_current_library(self, client, message):
        """Shows info for the current library that will play when no requests are given.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """

        if self.current_library is None:
            title = 'There is no current library'
            description = 'Use "!library set" to set a library to play inbetween requests'
        else:
            title = 'Here is the current library'
            description = 'Name: ' + self.current_library.name
            description += ' (by ' + self.current_library.author + ')'
            index = 1
            for song in self.current_library.songs:
                description += '\n' + str(index) + '. ' + song
                index += 1

        await self._create_embed(client, message, title, description)

    async def message_library_save_song(self, client, message):
        """Saves a song to the specified library.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """

        msg = message.content.replace('!library save ', '')
        song, library_name = msg.split(",")
        song = song.strip()
        library_name = library_name.strip()

        title, description = self.libraries.save_song(song, library_name)

        await self._create_embed(client, message, title, description)

    async def message_library_remove_song(self, client, message):
        """Removes a song from the specified library.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """

        msg = message.content.replace('!library remove ', '')
        song, library_name = msg.split(",")
        song = song.strip()
        library_name = library_name.strip()

        title, description = self.libraries.remove_song(library_name, song)
        await self._create_embed(client, message, title, description)

    async def message_quit(self, client):
        """Removes the Bot from the voice channel, also
           makes the queue empty again.

        Args:
            client (Client): client object from Discord
        """
        if self.song_queue.length_queue() > 0:
            self.song_queue.clear_queue()
            self.song_queue.add_song('null')
            await self.message_skip(client)

    async def message_restart(self, client):
        """Restarts the song that is currently playing"""
        self.song_queue.insert_song(0, self.song_queue.get_song(0))
        await self.message_skip(client)

    async def help(self, client, message):
        """prints an embed message with help statements
           for all available commands.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        msg = "play album - plays an album. input is as"
        msg += " \"!play album, artist\""

        msg += "\nplay playlist - plays a playlist from spotify. input as:"
        msg += " \"!play playlist, username\""

        msg += "\nplay - plays a single song from youtube."
        msg += " input as: \"!play songInfo\""

        msg += "\nqueue - returns the music queue"

        msg += "\nhistory - returns the previous 10 songs a user has played."
        msg += " input as \"!history\" or \"!history username\""

        msg += "\nrepeat - repeats the song that is playing."
        msg += "input as \"!repeat song_name\""

        msg += "\nskip - skips current song playing. input as \"!skip\""

        msg += "\nremove song - removes the said song. input as"
        msg += " \"!remove song_name\""

        msg += "\nquit - removes bot from voice channel, and"
        msg += "restarts the queue. input as \"!quit\""

        msg += "\nrestart - restarts the song that is currently playing."
        msg += "input as \"!restart\""

        msg += "\nrec get - gets a list of 20 songs recommended to"
        msg += " you based on your previous five queue'd songs."
        msg += " input as \"!rec get\""

        msg += "\nrec add - adds a list of 20 songs recommended"
        msg += " to you to the queue. input as \"!rec add\""

        await self._create_embed(client, message, description=msg)


# class Event_Ready:
#     # on_ready features here

# class Event_Reaction:
#     # on_reaction features here

# class Event_Server_Join:
#     # on_server_join features here

# class Event_Server_Remove:
#     # on_server_remove features here
