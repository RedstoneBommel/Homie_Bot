import discord
from discord import Interaction, Embed, app_commands, ButtonStyle, Color
from discord.ui import View, Button
from discord.ext import commands
import random
import json

def has_role(role_name):
    def predicate(interaction: Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class flagGuesser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    member = "Member"
    @app_commands.command(name = "flagGuesser", description = "Do you know every country and there flag?")
    @has_role(member)
    async def flagGuesser(self, interaction: Interaction, rounds: int = None):
        if rounds == None:
            rounds = 10
        with open("json/flagGuesser.json", "r") as flag_json:
            flagGuesserData = json.load(flag_json)
            