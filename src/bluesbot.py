# Work with Python 3.6
import discord
from src import events

event_msg = events.Event_Message()

class BluesBot:
    async def on_message_start(self, client, message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return

        if message.content.startswith('!'):
            await event_msg.message_recieved(client, message)

    async def on_ready_start(self, client):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')


