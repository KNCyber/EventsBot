import discord
import json
from discord.ext import commands

f = open("../config.json")
config = json.loads(f.read())

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged on as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    eventChannel = client.get_channel(config['eventChannelId'])
    await eventChannel.send(f'Message sent by {message.author} : {message.content}')


client.run(config['token'])
