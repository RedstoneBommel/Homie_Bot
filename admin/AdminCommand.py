from datetime import datetime, timezone
from discord import app_commands
from discord.ext import commands
import json
import discord

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    adminRole = []

    with open("../json/admin.json", "r") as admin_data:
        if "adminRoles" in admin_data:
            for i in "adminRoles":
                adminRole.append(i)
        admin_data.close()

    @app_commands.command(name = "delete_messages", description = "Delete messages...")
    @has_role(adminRole)
    async def delete_messages(self, interaction: discord.Interaction, number: int, member: discord.Member = None):
        delete_counter = 0
        async for message in interaction.channel.history():
            if message.author == member or member == None:
                await message.delete()
                delete_counter += 1
            if delete_counter == number:
                if delete_counter == 1:
                    return(f"{delete_counter} message deleted.")
                else:
                    return(f"{delete_counter} messages deleted.")
    @deletemessages.error
    async def messages_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(str(error), ephemeral = True)
    
    @app_commands.command(name = "ban", description = "Ban an User")
    @has_role(adminRole)
    async def ban(self, interaction: discord.Interaction, member: discord.User, reason: str = None):
        bannedUsers = []

        try:
            with open("../json/banns.json", "r") as ban_data:
                bannedUsers = json.load(ban_data)
        except FileNotFoundError:
            pass

        bannedUser = {
            "name": member.name,
            "id": member.id,
            "reason": reason
        }
        bannedUsers.append(bannedUser)

        with open("../json/banns.json", "w") as ban_data:
            json.dump(bannedUsers, ban_data)
        
        guild = interaction.guild
        await guild.ban(member, reason = reason)             