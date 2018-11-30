# Work with Python 3.6

# third-party
import discord

# local
from src import events
from src.queue import SongQueue


class BluesBot:
    """Class to create the bot object
    
    Attributes:
        stopper (Stop_Sign): object to see if song is playing or not
        song_queue (SongQueue): song queue object to handle all queue interactions
        event_msg (event): the message sent in discord
    """
    def __init__(self, stopper):
        self.stopper = stopper
        self.song_queue = SongQueue()
        self.event_msg = events.Event_Message(self.song_queue)

    async def on_message_start(self, client, message):
        """Handles the on-message-event

        Args:
            client (Client): client object for discord
            message (Message): message object from discord
        
        Returns:
            None: if the author is the bot
        """
        if message.author == client.user:
            return

        if message.content.startswith('!'):
            await self.event_msg.message_recieved(client, message, self.stopper)

    async def on_ready_start(self, client):
        """Tells the user when the bot is ready to go
        
        Args:
            client (Client): client object for discord
        """
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
