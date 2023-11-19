from discord import app_commands
from discord.ext import commands
import json
import discord

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    everyone = "@everyone"

    # Rules Channel Detection
    @app_commands.command(name = "rules", description = "Shows you the rules channel")
    @has_role(everyone)
    async def rules(self, interaction: discord.Interaction):
        member = interaction.user
        ruleChannel = []
        with open("json/admin.json", "r") as admin_data:
            channels = json.load(admin_data)
        if "ruleChannel" in channels:
            for i in "ruleChannel":
                ruleChannel.append(i)
            await interaction.response.send_message(f"{member.mention} you will find the rules in {ruleChannel[0].mention}")
            return ruleChannel[0]
        channelList = [channel.name for channel in interaction.guild.channels]
        channelNamePart = []
        for channel in channelList:
            channelNamePart.append(channel)
            ruleTitles = ["rule", "rules", "Regeln", "regeln"]
            for part in channelNamePart:
                for title in ruleTitles:
                    if title == part:
                        ruleChannel.append(channel)
                        with open("json/admin.json", "r+") as admin_data:
                            data = json.load(admin_data)
                            data["ruleChannel"] = channel
                            admin_data.seek(0)
                            json.dump(data, admin_data)
                        await interaction.response.send_message(f"{member.mention} you will find the rules in {ruleChannel[0].mention}")
                        return ruleChannel[0]
        await interaction.response.send_message(f"{member.mention} there isn't any channel with rules. May ask an server admin.")
        return "no rules channel found"
        

async def setup(bot):
    await bot.add_cog(info(bot))