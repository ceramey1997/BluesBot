import discord
import asyncio
from spotify_plugin import bot_plugin

song_queue = {}
spotify_object = bot_plugin()
class Event_Message:
    async def message_recieved(self, client, message):
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

        if message.content.startswith('!queue'):
            await self.message_queue(client, message)

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
        song_queue[message] =  album_info
        msg = '"' + message + '" has been added to the song queue'
        await client.send_message(channel, msg)

    async def message_play_playlist(self, client, message, channel):
        playlist, username = message.split(',')
        playlist = playlist.strip()
        username = username.strip()
        playlist_info = spotify_object.get_playlist(playlist, username)
        song_queue[playlist] = playlist_info
        msg = '"' + playlist + '" has been added to the song queue'
        print(song_queue)
        await client.send_message(channel, msg)

    async def message_queue(self, client, message):
        index = 1
        msg = 'The current song queue is:'
        for key in song_queue:
            msg += '\n ' + str(index) + '. ' + key
            index += 1

        await client.send_message(message.channel, msg)

    async def join(self, client, message):
        channel = client.get_channel('501955815222149154')
        await client.join_voice_channel(channel)

    async def help(self, client, message):
        msg = "!play - plays an album. input is as \"!play album,artist\""
        msg = msg + "\n!queue - returns the music queue"
        msg = msg + "\n!join - joins the general channel\n!hello - says hello back"
        await client.send_message(message.channel, msg)
