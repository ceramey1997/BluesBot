"""Handles the starting up of the bot"""
# Work with Python 3.6
import json
import logging

import os
import discord
from blues_bot.src.bluesbot import BluesBot
from blues_bot.src.commands import Commands
from discord.ext import commands


# pylint: disable=C0103
# client = discord.Client()
bot = commands.Bot(command_prefix='!')
bot_commands = Commands()

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

FILE_OBJECT = open('creds.json', 'r')
CREDS = json.loads(FILE_OBJECT.read())
FILE_OBJECT.close()
TOKEN = CREDS['DISCORD_TOKEN']

@bot.event
async def on_ready():
    """starts bot on ready"""
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name='hello', pass_context=True)
async def hello(ctx):
    await bot_commands.hello(bot, ctx)

@bot.command(name='quit', pass_context=True)
async def quit(ctx):
    await bot_commands.quit(bot, ctx)

@bot.command(name='offline', pass_context=True)
async def offline(ctx):
    await bot_commands.offline(bot, ctx)

@bot.command(name='play', pass_context=True)
async def play(ctx):
    await bot_commands.play(bot, ctx)

@bot.command(name='skip', pass_context=True)
async def skip(ctx):
    await bot_commands.skip(bot)

@bot.command(name='queue', pass_context=True)
async def queue(ctx):
    await bot_commands.queue(bot, ctx)

@bot.command(name='song', pass_context=True)
async def song(ctx):
    await bot_commands.song(bot, ctx)

@bot.command(name='history', pass_context=True)
async def history(ctx):
    await bot_commands.history(bot, ctx)

@bot.command(name='volume', pass_context=True)
async def volume(ctx):
    await bot_commands.volume(bot, ctx)

bot.run(TOKEN)
