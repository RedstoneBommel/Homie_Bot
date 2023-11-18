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
    
    # Add / Remove role from a user
    @app_commands.command(name = "role", description = "Add a role or remove a role from a user")
    @has_role(adminRole)
    async def role(self, interaction: discord.Interaction, role: discord.Role, action: str, member: discord.Member):
        if action == "add":
            with open("json/member.json", "r") as admin_data:
                memberJSON = json.load(admin_data)
            for roles in memberJSON[member.name]['roles']:
                if role == roles:
                    interaction.response.send_message("The user already has the role.")
                    return "role already assigned to user"
            await member.add_roles(role)
        elif action == "remove":
            with open("json/member.json", "r") as admin_data:
                memberJSON = json.load(admin_data)
            for roles in memberJSON[member.name]['roles']:
                if role == roles:
                    await member.remove_roles(role)
            interaction.response.send_message("The user doesn't have the role.")
            return "role is not assigned to user"
        else:
            await interaction.response.send_message("You don't use an official action")
            return "wrong action"
    
    # Create / Delete roles
    @app_commands.command(name = "add_role", description = "Add a role to the guild")
    @has_role(adminRole)
    async def add_role(self, interaction: discord.Interaction, role: str):
        await interaction.guild.create_role(name = role)
    @app_commands.command(name = "delete_role", description = "Delete a role from the guild")
    @has_role(adminRole)
    async def delete_role(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.guild._remove_role(name = role)
    
async def setup(bot):
    await bot.add_cog(roles(bot))