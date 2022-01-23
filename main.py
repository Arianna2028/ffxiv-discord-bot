import os

import discord
from dotenv import load_dotenv

from bot.models.roulette import Roulette, RouletteType
from bot.roulette import random_by_role
from bot.services.xivapi import XIVAPIService
from bot.util.discord import parse_character_name

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
START_SYMBOL = "$"  # Symbol commands must start with to be recognized
api_service = XIVAPIService(os.getenv("XIVAPI_KEY"))


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.content.startswith(START_SYMBOL):
        return

    if message.content.startswith(f"{START_SYMBOL}ping"):
        await message.channel.send("pong")

    if message.content.startswith(f"{START_SYMBOL}roulette"):
        channel = message.author.voice.channel
        users = channel.members
        character_names = [parse_character_name(u.nick) for u in users]
        character_ids = [api_service.character_id_from_name(c) for c in character_names]
        characters = [api_service.character_from_id(c.lodestone_id) for c in character_ids]
        leveling_roulette = Roulette(
            name=RouletteType.LEVELING,
            num_tanks=1,
            num_healers=1,
            num_dps=2,
            min_job_level=16,
        )

        selections = random_by_role(roulette=leveling_roulette, characters=characters)
        response = discord.Embed(title="Assigned Jobs")
        for selection in selections:
            emoji = discord.utils.get(message.guild.emojis, name=selection.job.short_name)
            response.add_field(name=selection.character.name, value=f"{emoji} {selection.job.name}")
        await message.channel.send(embed=response)


client.run(TOKEN)
