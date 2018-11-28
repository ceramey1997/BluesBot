# Work with Python 3.6
import discord
import events

TOKEN = 'NTE3MzY1NTcwMjg3Njk3OTIy.DuBKKQ.Ge6SrYlpjfxv7s7vRdjiyYC3TRI'

client = discord.Client()
event_msg = events.Event_Message()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        await event_msg.message_recieved(client, message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
#server = discord.Server()
#client.get_server(server)

