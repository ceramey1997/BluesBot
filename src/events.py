import discord
import asyncio

song_queue = {}

class Event_Message:
    async def message_recieved(self, client, message):
        if message.content.startswith('!hello'):
            await self.message_hello(client, message)

        if message.content.startswith('!play'):
            await self.message_play(client, message)

        if message.content.startswith('!queue'):
            await self.message_queue(client, message)

        if message.content.startswith('!join'):
            await self.join(client, message)

    async def message_hello(self, client, message):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    async def message_play(self, client, message):
        song_queue[message.content[5:]] =  'url'
        msg = '"' + message.content[5:] + '" has been added to the song queue'
        await client.send_message(message.channel, msg)

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
