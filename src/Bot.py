import discord
import json
import os
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class EveryonePromptView(discord.ui.View):

    def __init__(self, modal_input: dict):
        super().__init__(timeout=None)
        self.modal_input = modal_input

    @discord.ui.button(label="@everyone ???", style=discord.ButtonStyle.success)
    async def set_bool_true(self, interaction: discord.Interaction, self_item) -> None:
        await send_event(self.modal_input, True)
        await interaction.response.send_message(
            f"Event {self.modal_input.get('meetingTitle')} sent to the channel successfully", ephemeral=True)
        self.stop()

    @discord.ui.button(label="No ping", style=discord.ButtonStyle.red)
    async def set_bool_false(self, interaction: discord.Interaction, self_item) -> None:
        await send_event(self.modal_input, False)
        await interaction.response.send_message(
            f"Event {self.modal_input.get('meetingTitle')} sent to the channel successfully", ephemeral=True)
        self.stop()


class EventModal(discord.ui.Modal, title="Quack"):
    meetingTitle = discord.ui.TextInput(label="Meeting title", placeholder="reversing?", required=True)
    description = discord.ui.TextInput(label="Meeting description", placeholder="???", required=True)
    date = discord.ui.TextInput(label="What time is the meeting?", placeholder="Hope it isn't monday", required=True)
    room = discord.ui.TextInput(label="Do we have a place to sit?", placeholder="EITI 133?", required=True)
    beer = discord.ui.TextInput(label="BEER?", placeholder="I hope so", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        modal_input = dict(meetingTitle=self.meetingTitle.value,
                           description=self.description.value,
                           date=self.date.value,
                           room=self.room.value,
                           beer=self.beer.value)
        view = EveryonePromptView(modal_input=modal_input)
        await interaction.response.send_message(f"Event {self.meetingTitle} added successfully",
                                                ephemeral=True,
                                                view=view)
        await view.wait()


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
    if interaction.guild.get_role(int(os.getenv("role_id"))) in interaction.user.roles:
        await interaction.response.send_modal(EventModal())


async def send_event(modal_input, everyone):
    event_channel = bot.get_channel(int(os.getenv("event_channel_id")))
    event_message = create_event_message(modal_input=modal_input, everyone=everyone)
    await event_channel.send(event_message)


def create_event_message(modal_input: [], everyone):
    print(modal_input)
    modal_input.get("meetingTitle")
    isEveryone = "@everyone \t" if everyone else ""
    return f"{isEveryone}{modal_input.get('meetingTitle')}\n{modal_input.get('description')}\n\n\n{modal_input['room']},\t{modal_input['date']}\n\n{modal_input['beer']}\n\n"


bot.run(os.getenv("token"))
