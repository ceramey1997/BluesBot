# third-party
import discord


class User(discord.User):
    """Discord User class to keep up with current users in the
       Discord Server. for private Discord voice chat

    Attributes:
        user (discord.User): user object to keep up with who
                             is in the discord
        history (list): users song choice history
    """
    def __init__(self, user):
        super(discord.User, self).__init__()
        self.user = user
        self.history = []

class User(discord.Member):
    """Member User class to keep up with current users in the
       Discord Server. for public Discord voice chat

    Attributes:
        user (discord.Member): user object to keep up with who
                               is in the discord
        history (list): users song choice history
    """
    def __init__(self, user):
        super(discord.Member, self).__init__()
        self.user = user
        self.history = []

