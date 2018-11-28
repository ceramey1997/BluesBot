import discord
from  src.users import user

song_queue = {}
users = {}

class Event_Message:
    async def message_recieved(self, client, message):
        if message.author.name not in users:
            userIn = user.User(message.author)
            users[message.author.name] = userIn

        if message.content.startswith('!hello'):
            await self.message_hello(client, message)

        if message.content.startswith('!play'):
            await self.message_play(client, message)

        if message.content.startswith('!queue'):
            await self.message_queue(client, message)

        if message.content.startswith('!history'):
            await self.message_history(client, message)

    async def message_hello(self, client, message):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    async def message_play(self, client, message):
        song_queue[message.content[6:]] =  'url'
        users[message.author.name].history.insert(0, message.content[6:])
        msg = '"' + message.content[6:] + '" has been added to the song queue'
        await client.send_message(message.channel, msg)

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


