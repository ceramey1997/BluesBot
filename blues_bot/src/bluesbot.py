"""handles message input, bot object"""
# Work with Python 3.6
from blues_bot.src.events import EventMessage
from blues_bot.src.queue import SongQueue
from blues_bot.src.commands import Commands
from discord.ext import commands


class BluesBot:
    """Class to create the bot object

    Attributes:
        song_queue (SongQueue): song queue object to
                                handle all queue interactions
        event_msg (event): the message sent in discord
    """

    bot = commands.Bot(command_prefix='!')

    def __init__(self):
        self.song_queue = SongQueue()
        #self.event_msg = EventMessage(self.song_queue)
        self.commands_class = Commands()

    @bot.command(name='hello')
    async def hello(self, client, message):
        await commands_class._hello(client, message)

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

        #if message.content.startswith('!'):
        #    await self.event_msg.message_recieved(client, message)

    async def on_ready_start(self, client):
        """Tells the user when the bot is ready to go

        Args:
            client (Client): client object for discord
        """
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
