import discord

class User(discord.User):
    def __init__(self, user):
        super(discord.User, self).__init__()
        self.user = user
        self.history = []

class User(discord.Member):
    def __init__(self, user):
        super(discord.Member, self).__init__()
        self.user = user
        self.history = []

