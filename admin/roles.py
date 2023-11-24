from discord import app_commands
from discord.ext import commands
from discord import Color, Interaction, Role, Member
import discord
import json

def has_role(role_name):
    def predicate(interaction: Interaction):
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
    async def role(self, interaction: Interaction, role: Role, action: str, member: Member):
        if action == "add":
            with open("json/member.json", "r") as admin_data:
                memberJSON = json.load(admin_data)
            for roles in memberJSON[member.name]['roles']:
                if role == roles:
                    interaction.response.send_message("The user already has the role.")
                    return "role already assigned to user"
            await interaction.response.send_message(f"{member.mention} got the role {role.mention}")
            await member.add_roles(role)
            with open("json/member.json", "w") as admin_data:
                memberJSON = json.load(admin_data)
                memberJSON[member.name]['roles'].append(role.name)
                admin_data.write(json.dumps(memberJSON))
                admin_data.close()
        elif action == "remove":
            with open("json/member.json", "r") as admin_data:
                memberJSON = json.load(admin_data)
            for roles in memberJSON[member.name]['roles']:
                if role == roles:
                    await member.remove_roles(role)
                    with open("json/member.json", "w") as admin_data:
                        memberJSON = json.load(admin_data)
                        memberJSON[member.name]['roles'].remove(role.name)
                        admin_data.write(json.dumps(memberJSON))
                        admin_data.close()
            interaction.response.send_message("The user doesn't have the role.")
            return "role is not assigned to user"
        else:
            await interaction.response.send_message("You don't use an official action")
            return "wrong action"
    
    # Create / Delete roles
    @app_commands.command(name = "add_role", description = "Add a role to the guild")
    @has_role(adminRole)
    async def add_role(self, interaction: Interaction, role: str, color: str):
        with open("json/color.json", "r") as admin_data:
            colors = json.load(admin_data)
        for hex in colors:
            if hex == color:
                color = colors[hex]
                color = discord.Color(int(color, 16))
        for roles in interaction.guild.roles:
            if role == roles.name:
                await interaction.response.send_message("Role exists in guild already", delete_after = 5)
                return "Role already exists"
        await interaction.guild.create_role(name = role, color = color)
        for roles in interaction.guild.roles:
            print(roles)
            if role == roles.name:
                await interaction.response.send_message(f"{roles.mention} is created successfully", delete_after = 5)
    @app_commands.command(name = "delete_role", description = "Delete a role from the guild")
    @has_role(adminRole)
    async def delete_role(self, interaction: Interaction, role: Role):
        await interaction.response.send_message(f"{role.mention} is deleted now", delete_after = 5)
        await role.delete()
async def setup(bot):
    await bot.add_cog(roles(bot))