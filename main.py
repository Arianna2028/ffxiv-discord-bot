import logging
import os

import discord
from dotenv import load_dotenv

from bot.models.roulette import RouletteType
from bot.roulette import random_by_role, roulette_by_type
from bot.services.xivapi import XIVAPIService
from bot.util.discord import parse_character_name

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
START_SYMBOL = "$"  # Symbol commands must start with to be recognized
api_service = XIVAPIService(os.getenv("XIVAPI_KEY"))

logger = logging.getLogger(__name__)


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.content.startswith(START_SYMBOL):
        return

    if message.content.startswith(f"{START_SYMBOL}ping"):
        await message.channel.send("pong")

    if message.content.startswith(f"{START_SYMBOL}roulette"):
        message_parts = message.content.split(" ")
        channel = message.author.voice.channel
        users = channel.members
        character_names = [parse_character_name(u.nick) for u in users]
        character_ids = [api_service.character_id_from_name(c) for c in character_names]
        characters = [api_service.character_from_id(c.lodestone_id) for c in character_ids]

        try:
            roulette_type = RouletteType(message_parts[1])
        except Exception as e:
            logger.info(f"Failed to parse RouletteType {message_parts[1]}: {e}")
            await message.channel.send(f"Invalid roulette type: {message_parts[1]}")
            return

        if not (roulette := roulette_by_type(roulette_type)):
            await message.channel.send(f"No roulette found with name {roulette_type}")
            return

        selections = random_by_role(roulette=roulette, characters=characters)
        response = discord.Embed(title="Assigned Jobs")
        for selection in selections:
            emoji = discord.utils.get(message.guild.emojis, name=selection.job.short_name)
            response.add_field(name=selection.character.name, value=f"{emoji} {selection.job.name}")
        await message.channel.send(embed=response)


logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
logger.info("Starting bot...")
client.run(TOKEN)
