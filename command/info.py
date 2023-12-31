from discord import app_commands, Embed, Color, Interaction, Member
from discord.ext import commands
import json
import discord

def has_role(role_name):
    def predicate(interaction: Interaction):
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
    async def rules(self, interaction: Interaction):
        member = interaction.user
        with open("json/admin.json", "r") as admin_data:
            channels = json.load(admin_data)
        if "rules" in channels and channels["rules"] != "None":
            ruleChannel = channels["rules"]
            discordRuleChannel = interaction.guild.channels
            for channel in discordRuleChannel:
                if channel.id == ruleChannel:
                    await interaction.response.send_message(f"{member.mention} you will find the rules in {channel.mention}")
                    return ruleChannel
        channelList = [channel for channel in interaction.guild.channels]
        ruleTitles = ["rule", "rules", "Rules", "Rule", "Regeln", "regeln"]
        for channel in channelList:
                for title in ruleTitles:
                    if title == channel.name:
                        with open("json/admin.json", "r+") as admin_data:
                            data = json.load(admin_data)
                            data["ruleChannel"] = channel.name
                            admin_data.seek(0)
                            json.dump(data, admin_data)
                        await interaction.response.send_message(f"{member.mention} you will find the rules in {channel.mention}")
                        return channel.name
        await interaction.response.send_message(f"{member.mention} there isn't any channel with rules. May ask an server admin.")
        return "no rules channel found"
    # Information about every single user
    @app_commands.command(name = "info", description = "Show information about users")
    @has_role(everyone)
    async def info(self, interaction: Interaction, member: Member = None):
        if member is None:
            member = interaction.user
        with open("json/member.json", "r+") as member_data:
            member_data = json.load(member_data)
            if str(member.name) in member_data:
                roles = member_data[member.name]["roles"]
                role_mentions = []
                serverRoles = interaction.guild.roles
                for role in roles:
                    for i in serverRoles:
                        if role == i.name:
                            role_mentions.append(i.mention)
            else:
                return f"{member} didn't exist"
        memberCard = Embed(title = f"Information about {member.name}")
        memberCard.color = Color.from_rgb(0, 255, 0)
        memberCard.set_thumbnail(url = member.display_avatar.url)
        memberCard.set_author(name = interaction.user, icon_url = interaction.user.display_avatar.url)
        memberCard.add_field(name = f"{member.name}", value = f"ID: {member.id}", inline = False)
        memberCard.add_field(name = "Member since:", value = member.joined_at.strftime("%d, %B, %Y"), inline = True)
        memberCard.add_field(name = "Status:", value = str(member.desktop_status), inline = True)
        memberCard.add_field(name = "Roles:", value = role_mentions, inline = False)
        memberCard.set_footer(text = "This embed was created by Homie")
        await interaction.response.send_message(embed = memberCard)

async def setup(bot):
    await bot.add_cog(info(bot))