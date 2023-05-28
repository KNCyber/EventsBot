import discord
import json
from discord.ext import commands

f = open("../config.json")
config = json.loads(f.read())

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class EventModal(discord.ui.Modal, title="Quack"):
    meetingTitle = discord.ui.TextInput(label="Meeting title", placeholder="reversing?", required=True)
    description = discord.ui.TextInput(label="Meeting description", placeholder="???", required=True)
    date = discord.ui.TextInput(label="What time is the meeting?", placeholder="Hope it isn't monday", required=True)
    room = discord.ui.TextInput(label="Do we have a place to sit?", placeholder="EITI 133?", required=True)
    beer = discord.ui.TextInput(label="BEER?", placeholder="I hope so", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        event_channel = bot.get_channel(config['eventChannelId'])
        event_message = create_event_message(self)
        await event_channel.send(event_message)
        await interaction.response.send_message(f"Event {self.meetingTitle} added successfully", ephemeral=True)


# Example of an event
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)


@bot.tree.command(name="event")
async def event(interaction: discord.Interaction):
    if interaction.guild.get_role(config['roleId']) in interaction.user.roles:
        await interaction.response.send_modal(EventModal())
    else:
        await interaction.response.send_message(f"You don't have the permission to execute this command", ephemeral=True)


def create_event_message(self):
    return f"@everyone \t{self.meetingTitle}\n{self.description}\n\n\n{self.room},\t{self.date}\n\n{self.beer}\n\n"


bot.run(config['token'])
