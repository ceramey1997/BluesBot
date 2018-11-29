# Work with Python 3.6
import discord
import src.bluesbot
import json
import logging
from src import bluesbot

log = logging.getLogger()
log.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s-%(message)s'))
log.addHandler(stream_handler)
file_handler = logging.FileHandler('discord.log',mode='a')
file_handler.set_name(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s-%(message)s'))
log.addHandler(file_handler)

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

