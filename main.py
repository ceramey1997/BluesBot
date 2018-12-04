"""Handles the starting up of the bot"""
# Work with Python 3.6
import json
import logging

import os
import discord
from blues_bot.src.bluesbot import BluesBot

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.WARNING)
STREAM_HANDLER.setFormatter(
    logging.Formatter('%(asctime)s-%(levelname)s-%(message)s'))
LOG.addHandler(STREAM_HANDLER)
FILE_HANDLER = logging.FileHandler('discord.log', mode='a')
FILE_HANDLER.set_name(logging.DEBUG)
FILE_HANDLER.setFormatter(
    logging.Formatter('%(asctime)s-%(levelname)s-%(message)s'))
LOG.addHandler(FILE_HANDLER)

# FILE_OBJECT = open('creds.json', 'r')
# CREDS = json.loads(FILE_OBJECT.read())
# FILE_OBJECT.close()

# TOKEN = CREDS['DISCORD_TOKEN']
TOKEN = os.environ['DISCORD_TOKEN']

# pylint: disable=C0103
client = discord.Client()
BOT = BluesBot()
# Figure out how to get the server without causing an infinite loop


@client.event
async def on_message(message):
    """handles incoming messages from discord"""
    await BOT.on_message_start(client, message)


@client.event
async def on_ready():
    """starts bot on ready"""
    await BOT.on_ready_start(client)


client.run(TOKEN)
