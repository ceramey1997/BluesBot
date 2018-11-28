# Work with Python 3.6
import discord
import src.bluesbot

TOKEN = 'NTE3MzY1NTcwMjg3Njk3OTIy.DuBKKQ.Ge6SrYlpjfxv7s7vRdjiyYC3TRI'

client = discord.Client()
bot = src.bluesbot.BluesBot()
#TODO: Figure out how to get the server without causing an infinite loop

@client.event
async def on_message(message):
    await bot.on_message_start(client, message)

@client.event
async def on_ready():
    await bot.on_ready_start(client)

client.run(TOKEN)

