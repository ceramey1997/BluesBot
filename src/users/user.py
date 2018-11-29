import discord

class User(discord.User):
    def __init__(self, user, history = []):
        super(discord.User, self).__init__()
        self.user = user
        self.history = history

class User(discord.Member):
    def __init__(self, user, history = []):
        super(discord.Member, self).__init__()
        self.user = user
        self.history = history

