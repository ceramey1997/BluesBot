import discord
import asyncio

class Event_Message:
    async def message_recieved(self, client, message):
        if message.content.startswith('!hello'):
            await self.message_hello(client, message)

        if message.content.startswith('!play'):
            await self.message_play(client, message)

    async def message_hello(self, client, message):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    async def message_play(self, client, message):
        msg = '"' + message.content[5:] + '" has been added to the song queue'
        await client.send_message(message.channel, msg)
