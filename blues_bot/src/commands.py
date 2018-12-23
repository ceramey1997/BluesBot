# Python Packages
import asyncio
import datetime

# Third party libraries
import discord
from discord.ext import commands
from spotipy.client import SpotifyException

# Local files
from blues_bot.src.stop_sign import StopSign
from blues_bot.src.queue import SongQueue
from blues_bot.src.search_engine import search_yt
from blues_bot.spotify_plugin import SpotifyPlugin
from blues_bot import spotify_exceptions
from blues_bot.src.users.user import User


class Commands:

    def __init__(self):
        self.voice_client = None
        self.player = None
        self.volume = .40
        self.stopper = StopSign(False)
        self.first_flag = False
        self.song_queue = SongQueue()
        self.sp_ob = SpotifyPlugin()
        self.users = {}

# -----------------------------------------------------------
# -----------------------------------------------------------
        
    async def hello(self, bot, ctx):
        """Messages an in chat hello message.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        await self._check_user(ctx)
        msg = 'Hello ' + ctx.message.author.name
        await bot.say(msg)

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def quit(self, bot, ctx):
        """Removes the Bot from the voice channel, also
           makes the queue empty again.

        Args:
            client (Client): client object from Discord
        """
        await self._check_user(ctx)
        if self.song_queue.length_queue() > 0:
            self.song_queue.clear_queue()
            self.song_queue.add_song('null')
            await self.skip(bot, ctx)

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def offline(self, bot, ctx):
        await self._check_user(ctx)
        await bot.say('Goodbye!')
        await bot.logout()
        await bot.close()

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def play(self, bot, ctx):
        await self._check_user(ctx)
        tries = 0
        while tries < 3:
            try:
                channel = ctx.message.channel
                if ctx.message.content.startswith('!play album'):
                    await self._play_album(bot, ctx)
                elif ctx.message.content.startswith('!play playlist'):
                    await self._play_playlist(bot, ctx)
                else:
                    await self._play_single_song(bot, ctx)
                break
            except SpotifyException:
                self.sp_ob.refresh_token()
                tries += 1
        assert tries < 3, 'Could not get token'

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def skip(self, bot, ctx):
        """Skips the current song that is playing.

        Args:
            client (Client): client object from Discord
        """
        await self._check_user(ctx)
        await self._change_status(bot, None)
        self.stopper.set_flag(True)

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def queue(self, bot, ctx):
        """Sends a message of what is on the current Queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        await self._check_user(ctx)
        index = 1
        title = 'The current song queue is:'
        msg = ''
        for song in self.song_queue.get_list():
            msg += '\n ' + str(index) + '. ' + song
            index += 1

        await self._create_embed(bot, ctx, title, msg)

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def song(self, bot, ctx):
        """Displays info of the current song

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        await self._check_user(ctx)
        if self.player is not None:
            title = self.player.title
            description = 'URL: ' + self.player.url
            description += '\nDuration: ' + str(datetime.timedelta(seconds=self.player.duration))
            description += '\nUploader: ' + self.player.uploader
            description += ', Date: ' + str(self.player.upload_date)
            description += '\nLikes: ' + "{:,}".format(self.player.likes)
            description += ', Disikes: ' + "{:,}".format(self.player.dislikes)
            description += '\nViews: ' + "{:,}".format(self.player.views)
            await self._create_embed(bot, ctx, title, description)

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def history(self, bot, ctx):
        """Sends a message in chat channel of the user's last 10 adds
           to the queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        await self._check_user(ctx)
        username = ''
        title = 'Here are the last 10 songs requested by '

        msg = ctx.message.content.strip().lower() == '!history '
        if ctx.message.content.strip().lower() == '!history':
            username = ctx.message.author.name
        else:
            for key in self.users:
                if msg == key:
                    username = key

        if not username:
            await bot.say('That user does not exist')
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
        await self._create_embed(bot, ctx, title, msg)

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def volume(self, bot, ctx):
        """Sets the volume of the player

        Args:
            message (Message): message object from Discord
        """
        volume = int(message.content.replace('!volume', ''))
        if self.player is not None and 0 <= volume <= 100:
            volume = volume / 100
            self.volume = volume
            self.player.volume = volume

# -----------------------------------------------------------
# -----------------------------------------------------------
# Private functions
# -----------------------------------------------------------
# -----------------------------------------------------------


    async def _create_embed(self, bot, ctx, title=None, description=None):
        embed = discord.Embed(title=title,
                              description=description,
                              colour=0xDEADBF)
        await bot.send_message(ctx.message.channel, embed=embed)

    async def _check_user(self, ctx):
        if ctx.message.author.name not in self.users:
            user_in = User(ctx.message.author)
            self.users[ctx.message.author.name] = user_in

    async def _join(self, bot, ctx):
        """joins a voice channel.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        server_id = ctx.message.author.server.id
        if not bot.is_voice_connected(bot.get_server(server_id)):
            voice_channel = ctx.message.author.voice.voice_channel
            if not voice_channel:
                title = "you don't seem to be in the channel"
                await bot.say(title)
                return None
            self.voice_client = await bot.join_voice_channel(voice_channel)
        self.voice_client = bot.voice_client_in(bot.get_server(server_id))

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def _create_player(self, bot, ctx,  query):
        """Creates a ytdl player for a requested search query

        Args:
            client (Client): client object from Discord
            query (String): youtube search input
            message (Message): message object from Discord
        """
        if self.voice_client is None:
            await self._join(bot, ctx)
        if self.voice_client is None:
            return None
        url = search_yt(query)
        self.player = await self.voice_client.create_ytdl_player(url)
        self.player.volume = self.volume

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def _wait_for_song(self):
        """Waits for song to be completed

        Args:
            player (Player): player object from Youtube_dl
        """
        # pylint: disable=W0612
        for i in range(int(self.player.duration)):
            await asyncio.sleep(1)
            if self.stopper.get_flag():
                self.player.stop()
                self.stopper.set_flag(False)
                break

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def _change_status(self, bot, song_name):
        """Changes the status of the bot
            (on the far right of discord where it shows
            what game user's are playing)

        Args:
            client (Client): client object from Discord
            song_name (Str): song name to play
        """
        await bot.change_presence(game=discord.Game(name=song_name))

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def _play_song(self, bot, ctx, query):
        """Takes a song and query's youtube and joins the server
           if necessary, and plays the song.

        Args:
            client (Client): client object from Discord
            query (Str): song name and artist to query youtube with
            message (Message): message object from Discord
        """
        self.first_flag = False
        await self._create_player(bot, ctx, query)
        if self.player is None:
            return
        self.player.start()
        await self._change_status(bot, self.player.title)

        await self._wait_for_song()
        self.song_queue.pop_song()
        if self.song_queue.length_queue() > 0:
            await self._play_song(bot, ctx, self.song_queue.get_song(0))
        else:
            await bot.say('Goodbye!')
            await self.voice_client.disconnect()
            self.first_flag = False
            await self._change_status(bot, None)

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def _play_single_song(self, bot, ctx):
        """Command that plays a single requested song
        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
        """
        song = ctx.message.content.replace('!play ', '')
        self.song_queue.add_song(song)
        self.users[ctx.message.author.name].history.insert(0, song)
        if self.song_queue.length_queue() == 1:
            await self._play_song(bot, ctx, song)

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def _play_album(self, bot, ctx):
        """Takes the input of an album and plays if first thing
           in queue otherwise adds to back of queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
            channel (Str): Chat channel that the user sent the message from
        """
        msg = ctx.message.content.replace('!play album ', '')
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
                # self.log.error(str(spot_error))
                print(spot_error.args)
                return
            await client.send_message(channel, msg)
            return
        for song in album_info:
            self.song_queue.add_song(song)
            self.users[ctx.message.author.name].history.insert(0, song)
            description += "\n" + song
            if self.song_queue.length_queue() == 1:
                self.first_flag = True

        title = "Songs Added To Queue:\n\tAlbum: "
        title += album + "\n\tArtist: " + artist
        await self._create_embed(bot, ctx, title, description)

        if self.first_flag:
            await self._play_song(bot, ctx, self.song_queue.get_song(0))

# -----------------------------------------------------------
# -----------------------------------------------------------

    async def _play_playlist(self, bot, ctx):
        """Takes the input of an playlist and plays if first thing
           in queue otherwise adds to back of queue.

        Args:
            client (Client): client object from Discord
            message (Message): message object from Discord
            channel (Str): Chat channel that the user sent the message from
        """
        msg = ctx.message.content.replace('!play playlist ', '')
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
                # self.log.error(str(spot_error))
                print(spot_error.args)
                return
            await bot.say(msg)
            return
        for song in playlist_info:
            self.song_queue.add_song(song)
            self.users[ctx.message.author.name].history.insert(0, song)
            description += '\n' + song
            if self.song_queue.length_queue() == 1:
                self.first_flag = True

        title = "Songs Added To Queue From:\n\t" + playlist
        await self._create_embed(bot, ctx,
                                 title, description)

        if self.first_flag:
            await self._play_song(bot, ctx, self.song_queue.get_song(0))

