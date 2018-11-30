import discord
from  src.users import user
from src.search_engine import search_yt
import asyncio
from spotify_plugin import bot_plugin, SpotifyError, AlbumError, ArtistError, PlaylistError, UserError

users = {}
song_queue = []
spotify_object = bot_plugin()
firstFlag = False
player = None

class Event_Message:

    async def message_recieved(self, client, message, stopper):
        if message.author.name not in users:
            userIn = user.User(message.author)
            users[message.author.name] = userIn

        if message.content.startswith('!hello'):
            await self.message_hello(client, message)

        if message.content.startswith('!play'):
            channel = message.channel
            if message.content.startswith('!play album'):
                await self.message_play_album(client, message, channel, stopper)
            elif message.content.startswith('!play playlist'):
                await self.message_play_playlist(client, message, channel, stopper)
            else:
                msg = message.content.replace('!play ', '')
                song_queue.append(msg)
                if len(song_queue) == 1:
                    users[message.author.name].history.insert(0, msg)
                    await self.message_play_song(client, msg, stopper, message)

        if message.content.startswith('!queue'):
            await self.message_queue(client, message)

        if message.content.startswith('!history'):
            await self.message_history(client, message)
        if message.content.startswith('!join'):
            await self.join(client, message)

        if message.content.startswith('!help'):
            await self.help(client, message)

        if message.content.startswith('!skip'):
            await self.message_pause(stopper)
        
        if message.content.startswith('!remove'):
            song = message.content.replace('!remove ', '')
            await self.remove_song(client, message, song)

        if message.content.startswith('!remove'):
            song = message.content.replace('!remove ', '')
            await self.remove_song(client, message, song)

        if message.content.startswith('!repeat'):
            await self.message_repeat(client, message)

    async def message_hello(self, client, message):
        msg = 'Hello {0.author.mention}'.format(message)
        await self.create_embed(client, message, None, msg)

    async def message_play_album(self, client, message, channel, stopper):
        msg = message.content.replace('!play album ', '')
        album, artist = msg.split(",")
        album = album.strip()
        artist = artist.strip()
        description = ''
        try:
            album_info = spotify_object.get_album_tracks(album, artist)
        except SpotifyError as e:
            if isinstance(e, AlbumError):
                msg = 'Invalid album name'
            elif isinstance(e, ArtistError):
                msg = 'Invalid artist name'
            else:
                print(e.args)
                return
            await client.send_message(channel, msg)
            return
        for song in album_info:
            song_queue.append(song)
            users[message.author.name].history.insert(0, song)
            description += "\n" + song
            if len(song_queue) == 1:
                global firstFlag
                firstFlag = True

        title = "Songs Added To Queue:\n\tAlbum: " + album + "\n\tArtist: " + artist
        await self.create_embed(client, message, title, description)

        if firstFlag:
            await self.message_play_song(client, song_queue[0], stopper, message)

        await self.change_status(client, msg)

    async def message_play_playlist(self, client, message, channel, stopper):
        msg = message.content.replace('!play playlist ', '')
        playlist, username = msg.split(',')
        playlist = playlist.strip()
        username = username.strip()
        description = ''
        try:
            playlist_info = spotify_object.get_playlist_tracks(playlist, username)
        except SpotifyError as e:
            if isinstance(e, PlaylistError):
                msg = 'Invalid playlist name'
            elif isinstance(e, UserError):
                msg = 'Invalid username'
            else:
                print(e.args)
                return
            await client.send_message(channel, msg)
            return
        for song in playlist_info:
            song_queue.append(song)
            users[message.author.name].history.insert(0, song)
            description += '\n' + song
            if len(song_queue) == 1:
                global firstFlag
                firstFlag = True

        title = "Songs Added To Queue From:\n\t" + playlist
        await self.create_embed(client, message, title, description)

        if firstFlag:
            await self.message_play_song(client, song_queue[0], stopper, message)

    async def message_queue(self, client, message):
        index = 1
        mention = message.author.mention

        title = mention + ' The current song queue is:'
        msg = ''
        for song in song_queue:
            msg += '\n ' + str(index) + '. ' + song
            index += 1

        await self.create_embed(client, message, title, msg)

    async def message_history(self, client, message):

        user = None
        title = 'Here are the last 10 songs requested by '

        if message.content.strip().lower() == '!history':
            user = message.author
        else:
            for key in users:
                if message.content[9:] == users[key].mention: #TODO: This doesn't work :(
                    user = users[key]

        if user is None:
            await client.send_message(message.channel, 'That user does not exist')
            return
        title +=  user.mention
        history = users[user.name].history
        msg = ''
        index = 0
        while index < 10:
            if index >= len(history):
                break
            msg += '\n ' + str(index + 1) + '. ' + history[index]
            index += 1
        await self.create_embed(client, message, title, msg)

    async def _join(self, client, message):
        server_id = message.author.server.id
        if not client.is_voice_connected(client.get_server(server_id)):
            voice_channel = message.author.voice.voice_channel
            if voice_channel == None:
                await self.create_embed(client, message, title="you don't seem to be in the channel")
                return None
            voice_client = await client.join_voice_channel(voice_channel)
        voice_client = client.voice_client_in(client.get_server(server_id))
        return voice_client

    async def message_play_song(self, client, query, stopper, message):
        global firstFlag
        global player
        voice_client = await self._join(client, message)
        if voice_client is None:
            return
        url = search_yt(query)
        player = await voice_client.create_ytdl_player(url)
        player.volume = 0.1
        player.start()
        await self.change_status(client, query)
        for i in range(int(player.duration)):
            await asyncio.sleep(1)
            if stopper.get_flag():
                player.stop()
                stopper.set_flag(False)
                break
        #await asyncio.sleep(int(player.duration))
        song_queue.pop(0)
        if len(song_queue) > 0:
            await self.message_play_song(client, song_queue[0], stopper, message)
        else:
            await voice_client.disconnect()
            firstFlag = False

    async def change_status(self, client, song_name):
        await client.change_presence(game=discord.Game(name=song_name))

    async def message_repeat(self, client, message):
        current_song = song_queue[0]
        song_queue.insert(1, current_song)
        msg = message.author.mention + ' ' + current_song + ' will be repeated'
        await client.send_message(message.channel, msg)

    async def create_embed(self, client, message, title=None, description=None):
        em = discord.Embed(title=title, description=description, colour=0xDEADBF)
        em.set_author(name='Blues Bot', icon_url=client.user.default_avatar_url)
        await client.send_message(message.channel, embed=em)

    async def message_pause(self, stopper):
        global player
        stopper.set_flag(True)

    async def remove_song(self, client, message, song_name):
        for song in song_queue:
            if song_name.lower() in song.lower():
                song_queue.remove(song)
                msg = song + " has been removed from the queue"
                await self.create_embed(client, message, title=msg)
                return
        msg = song + " is not found in the queue"
        await self.create_embed(client, message, title=msg)
'''
class Event_Ready:
    # on_ready features here

class Event_Reaction:
    # on_reaction features here

class Event_Server_Join:
    # on_server_join features here

class Event_Server_Remove:
    # on_server_remove features here
'''
