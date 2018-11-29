# Work with Python 3.6
import discord
import src.bluesbot
import json
from src import bluesbot

f = open('creds.json', 'r')
creds = json.loads(f.read())
f.close()

TOKEN = creds['DISCORD_TOKEN']

client = discord.Client()
bot = bluesbot.BluesBot()
#TODO: Figure out how to get the server without causing an infinite loop

@client.event
async def on_message(message):
    await bot.on_message_start(client, message)

@client.event
async def on_ready():
    await bot.on_ready_start(client)

client.run(TOKEN)

