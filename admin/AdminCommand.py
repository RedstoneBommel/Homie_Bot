from datetime import datetime, timezone
from discord import app_commands
from discord.ext import commands
import json
import discord
import os

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    adminRole = []

    with open("json/admin.json", "r") as admin_data:
        if "adminRoles" in admin_data:
            for i in "adminRoles":
                adminRole.append(i)
        admin_data.close()

    # Delete messages
    @app_commands.command(name = "delete_messages", description = "Delete messages")
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
    @delete_messages.error
    async def messages_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(str(error), ephemeral = True)
    
    # Ban/Unban User
    @app_commands.command(name = "ban", description = "Ban a user")
    @has_role(adminRole)
    async def ban(self, interaction: discord.Interaction, member: discord.User, reason: str = None):
        bannedUsers = []
        guild = interaction.guild

        try:
            with open("json/banns.json", "r") as ban_data:
                bannedUsers = json.load(ban_data)
        except FileNotFoundError:
            pass

        bannedUser = {
            "name": member.name,
            "id": member.id,
            "reason": reason
        }
        bannedUsers.append(bannedUser)

        with open("json/banns.json", "w") as ban_data:
            json.dump(bannedUsers, ban_data)
        
        await guild.ban(member, reason = reason)
        await interaction.response.send_message(f"User {member.name} ({member.id}) is banned now") 
    @app_commands.command(name = "unban", description = "Unban a user")
    @has_role(adminRole)      
    async def unban(self, interaction: discord.Interaction, member: discord.User):
        bannedUsers = []
        guild = interaction.guild

        try:
            with open("json/banns.json", "r") as file:
                bannedUsers = json.load(file)
        except FileNotFoundError:
            pass

        filteredUsers = [user for user in bannedUsers if user["id"] != member.id]

        if len(filteredUsers) == len(bannedUsers):
            await interaction.response.send_message(f"User {member.name} ({member.id}) isn't banned")
            return

        with open("Owners/banned_users.json", "w") as file:
            json.dump(filteredUsers, file)

        await guild.unban(member)
        await interaction.response.send_message(f"User {member.name} ({member.id}) is unbanned now")
    
    # Kick User
    @app_commands.command(name = "kick", description = "Kick a user")
    @has_role(adminRole)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        guild = interaction.guild

        await guild.kick(member, reason = reason) 
        await interaction.response.send_message(f"User {member.name} ({member.id}) is kicked now")
    
    # Mute/Unmute User
    @app_commands.command(name = "mute", description = "Mute a user")
    @has_role(adminRole)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        muteUsers = []
        permission = discord.PermissionOverwrite()
        permission.speak = False
        permission.send_messages = False

        try:
            with open("json/mute.json", "r") as mute_data:
                muteUsers = json.load(mute_data)
        except FileNotFoundError:
            pass

        muteUser = {
            "name": member.name,
            "id": member.id,
            "reason": reason
        }
        muteUsers.append(muteUser)

        with open("json/mute.json", "w") as mute_data:
            json.dump(muteUsers, mute_data)

        for channel in interaction.guild.channels:
            if isinstance(channel, discord.VoiceChannel) or isinstance(channel, discord.TextChannel):
                await channel.set_permissions(member, overwrite = permission)
                muteUsers[str(member.id)]["voiceChannel"].append(channel.id) if isinstance(channel, discord.VoiceChannel) else muteUsers[str(member.id)]["textChannel"].append(channel.id)
                await interaction.response.send_message(f"User {member.name} ({member.id}) is muted now")
    @app_commands.command(name = "unmute", description = "Unmute a user")
    @has_role(adminRole)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        muteUsers = []
        permission = discord.PermissionOverwrite()
        permission.speak = True
        permission.send_messages = True

        try:
            with open("json/mute.json", "r") as mute_data:
                muteUsers = json.load(mute_data)
        except FileNotFoundError:
            pass

        filteredUsers = [user for user in muteUsers if user["id"] != member.id]

        if len(filteredUsers) == len(muteUsers):
            return(f"User {member.name} ({member.id}) isn't muted")

        with open ("json/mute.json", "w") as mute_data:
            json.dump(filteredUsers, mute_data)

        for channel in interaction.guild.channels:
            if isinstance(channel, discord.VoiceChannel) or isinstance(channel, discord.TextChannel):
                await channel.set_permissions(member, overwrite = permission)
        
        await interaction.response.send_message(f"{member.mention} your aren't muted anymore")

async def setup(bot):
    await bot.add_cog(admin(bot))
