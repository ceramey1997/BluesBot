import discord
from  src.users import user
from src.search_engine import search_yt
import asyncio
from spotify_plugin import bot_plugin

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
                await self.message_play_album(client, message, channel)
            elif message.content.startswith('!play playlist'):
                await self.message_play_playlist(client, message, channel)
            else:
                msg = message.content.replace('!play ', '')
                song_queue.append(msg)
                if len(song_queue) == 1:
                    users[message.author.name].history.insert(0, msg)
                    await self.message_play_song(client, message.content, stopper)

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

    async def message_hello(self, client, message):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    async def message_play_album(self, client, message, channel):
        msg = message.content.replace('!play album ', '')
        album, artist = msg.split(",")
        album = album.strip()
        artist = artist.strip()
        album_info = spotify_object.get_album(album, artist)
        for song in album_info:
            song_queue.append(song)
            users[message.author.name].history.insert(0, song)
            if len(song_queue) == 1:
                global firstFlag
                firstFlag = True
        if firstFlag:
            await self.message_play_song(client, song_queue[0])
        msg = '"' + album + ", " + artist + '" has been added to the song queue'
        await client.send_message(channel, msg)

    async def message_play_playlist(self, client, message, channel):
        msg = message.content.replace('!play playlist ', '')
        playlist, username = msg.split(',')
        playlist = playlist.strip()
        username = username.strip()
        playlist_info = spotify_object.get_playlist(playlist, username)
        for song in playlist_info:
            song_queue.append(song)
            users[message.author.name].history.insert(0, song)
            if len(song_queue) == 1:
                global firstFlag
                firstFlag = True
        if firstFlag:
            await self.message_play_song(client, song_queue[0])
        msg = '"' + playlist + '" has been added to the song queue'
        await client.send_message(channel, msg)

    async def message_queue(self, client, message):
        index = 1
        msg = 'The current song queue is:'
        for song in song_queue:
            msg += '\n ' + str(index) + '. ' + song
            index += 1

        await client.send_message(message.channel, msg)

    async def message_history(self, client, message):
        msg = 'Here are the last 10 songs requested by '
        username = ''
        if message.content.strip().lower() == '!history':
            username = message.author.name
        elif message.content[9:] == 'me':
            username = message.author.name
        else:
            for key in users:
                if message.content[9:] == key:
                    username = message.content[9:]

        if username == '':
            await client.send_message(message.channel, 'That user does not exist')
            return
        msg +=  username
        index = 0
        history = users[username].history
        while index < 10:
            if index >= len(history):
                break
            msg += '\n ' + str(index + 1) + '. ' + history[index]
            index += 1
        await client.send_message(message.channel, msg)

    async def _join(self, client):
        if not client.is_voice_connected(client.get_server('501955815222149150')):
            channel = client.get_channel('501955815222149154')
            voice_client = await client.join_voice_channel(channel)
        voice_client = client.voice_client_in(client.get_server('501955815222149150'))
        return voice_client

    async def message_play_song(self, client, query, stopper):
        global firstFlag
        global player
        voice_client = await self._join(client)
        url = search_yt(query)
        player = await voice_client.create_ytdl_player(url)
        player.start()
        for i in range(int(player.duration)):
            await asyncio.sleep(1)
            if stopper.get_flag():
                player.stop()
                stopper.set_flag(False)
                break
        #await asyncio.sleep(int(player.duration))
        song_queue.pop(0)
        if len(song_queue) > 0:
            await self.message_play_song(client, song_queue[0], stopper)
            await self.change_status(query)
        else:
            firstFlag = False

    async def change_status(self, client, song_name):
        await client.change_presence(game=discord.Game(name=song_name))

    async def message_pause(self, stopper):
        global player
        stopper.set_flag(True)

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
