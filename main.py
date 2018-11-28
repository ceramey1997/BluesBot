# Work with Python 3.6
import discord
import events

TOKEN = 'NTE3MzY1NTcwMjg3Njk3OTIy.DuBKKQ.Ge6SrYlpjfxv7s7vRdjiyYC3TRI'

client = discord.Client()
event_msg = events.Event_Message()

@client.event
async def on_message(message):
    await on_message_start()

@client.event
async def on_ready():
    await on_ready_start()

client.run(TOKEN)

