# Work with Python 3.6
import discord
from src import events
from src.queue import SongQueue


class BluesBot:
    def __init__(self, stopper):
        self.stopper = stopper
        self.song_queue = SongQueue()
        self.event_msg = events.Event_Message(self.song_queue)

    async def on_message_start(self, client, message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return

        if message.content.startswith('!'):
            await self.event_msg.message_recieved(client, message, self.stopper)

    async def on_ready_start(self, client):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
