import discord
from  src.users import user
from src.search_engine import search_yt
import asyncio
from spotify_plugin import bot_plugin

users = {}
song_queue = []
spotify_object = bot_plugin()

class Event_Message:
    async def message_recieved(self, client, message):
        if message.author.name not in users:
            userIn = user.User(message.author)
            users[message.author.name] = userIn

        if message.content.startswith('!hello'):
            await self.message_hello(client, message)

        if message.content.startswith('!play'):
            channel = message.channel
            msg = message.content.replace('!play ', '')
            if msg.startswith('album'):
                msg = msg.replace('album ', '')
                await self.message_play_album(client, msg, channel)
            elif msg.startswith('playlist'):
                msg = msg.replace('playlist ', '')
                await self.message_play_playlist(client, msg, channel)
            else:
                await self.message_play_song(client, msg)
        
            users[message.author.name].history.insert(0, msg)


        if message.content.startswith('!queue'):
            await self.message_queue(client, message)

        if message.content.startswith('!history'):
            await self.message_history(client, message)
        if message.content.startswith('!join'):
            await self.join(client, message)

        if message.content.startswith('!help'):
            await self.help(client, message)

    async def message_hello(self, client, message):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    async def message_play_album(self, client, message, channel):
        album, artist = message.split(",")
        album = album.strip()
        artist = artist.strip()
        album_info = spotify_object.get_album(album, artist)
        for song in album_info:
            song_queue.append(song)
        msg = '"' + message + '" has been added to the song queue'
        await client.send_message(channel, msg)

    async def message_play_playlist(self, client, message, channel):
        playlist, username = message.split(',')
        playlist = playlist.strip()
        username = username.strip()
        playlist_info = spotify_object.get_playlist(playlist, username)
        for song in playlist_info:
            song_queue.append(song)
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

    async def message_play_song(self, client, query):
        voice_client = await self._join(client)
        url = search_yt(query)
        song_queue.append(query)
        player = await voice_client.create_ytdl_player(url)
        player.start()

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
