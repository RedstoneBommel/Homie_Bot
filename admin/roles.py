from discord import app_commands
from discord.ext import commands
import discord
import json

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    adminRole = []

    with open("json/admin.json", "r") as admin_data:
        if "adminRoles" in admin_data:
            for i in "adminRoles":
                adminRole.append(i)
        admin_data.close()
    
    @app_commands.command(name = "role", description = "Add a role or remove a role from a user")
    @has_role(adminRole)
    async def role(self, interaction: discord.Interaction, role: discord.Role, action: str, member: discord.Member):
        if action == "add":
            with open("json/member.json", "r") as admin_data:
                memberJSON = json.load(admin_data)
            for roles in memberJSON[member.name]['roles']:
                print("check")
                if role == roles:
                    interaction.response.send_message("The user already has the role.")
                    return "role already assigned to user"
            await member.add_roles(role)
            interaction.response.send_message("Role added successfully.")
            return "role added successfully"
        elif action == "remove":
            with open("json/member.json", "r") as admin_data:
                memberJSON = json.load(admin_data)
            for roles in memberJSON[member.name]['roles']:
                if role == roles:
                    await member.remove_roles(role)
                    interaction.response.send_message("Role removed successfully.")
                    return "role removed from user"
            interaction.response.send_message("The user doesn't have the role.")
            return "role is not assigned to user"
        else:
            await interaction.response.send_message("You don't use an official action")
            return "wrong action"

async def setup(bot):
    await bot.add_cog(roles(bot))