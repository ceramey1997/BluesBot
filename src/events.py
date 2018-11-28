import discord
<<<<<<< HEAD
from  src.users import user

song_queue = {}
users = {}

=======
import asyncio
from spotify_plugin import bot_plugin

song_queue = {}
spotify_object = bot_plugin()
>>>>>>> eb3d3b40f696fb1b95901f1cb1c0796288a1d7cb
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

    async def message_play(self, client, message):
        song_queue[message.content[6:]] =  'url'
        users[message.author.name].history.insert(0, message.content[6:])
        msg = '"' + message.content[6:] + '" has been added to the song queue'
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

    async def message_history(self, client, message):
        msg = 'Here are the last 10 songs requested by '
        username = ''
        if message.content[9:] == 'me':
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


