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
    @app_commands.command(name="role", description="Add a role or remove a role from a user")
    @has_role(adminRole)
    async def role(self, interaction: Interaction, role: Role, action: str, member: Member):
        role = role
        if action == "add":
            with open("json/member.json", "r") as admin_data:
                memberJSON = json.load(admin_data)
                memberJSON[member.name]['roles']
                try:
                    print(memberJSON[member.name]['roles'])
                except UnicodeEncodeError:
                    print("Unable to print member_roles due to an unsupported Unicode character.")
                for roles in memberJSON[member.name]['roles']:
                    if role.name == roles:
                        await interaction.response.send_message(f"{member.mention} hat bereits die Rolle {role.mention}.")
                        return "Rolle bereits dem Benutzer zugewiesen"
                await interaction.response.send_message(f"{member.mention} hat die Rolle {role.mention} erhalten.")
                await member.add_roles(role)
                memberJSON[member.name]['roles'].append(role.name)
                try:
                    print(memberJSON[member.name]['roles'])
                except UnicodeEncodeError:
                    print("Unable to print member_roles due to an unsupported Unicode character.")
            with open("json/member.json", "w") as admin_data:
                json.dump(memberJSON, admin_data)
                admin_data.close()
        elif action == "remove":
            with open("json/member.json", "r") as admin_data:
                memberJSON = json.load(admin_data)
                memberJSON[member.name]['roles']
                try:
                    print(memberJSON[member.name]['roles'])
                except UnicodeEncodeError:
                    print("Unable to print member_roles due to an unsupported Unicode character.")
                for roles in memberJSON[member.name]['roles']:
                    if role.name == roles:
                        await member.remove_roles(role)
                        memberJSON[member.name]['roles'].remove(role.name)
                        with open("json/member.json", "w") as admin_data:
                            json.dump(memberJSON, admin_data)
                            admin_data.close()
                        await interaction.response.send_message(f"{role.mention} wurde von {member.mention} entfernt.")
                        return "Rolle vom Benutzer entfernt"
            await interaction.response.send_message(f"{member.mention} hat die Rolle {role.mention} nicht.")
            return "Rolle ist dem Benutzer nicht zugewiesen"
        else:
            await interaction.response.send_message("Sie verwenden keine offizielle Aktion.")
            return "Falsche Aktion"
        
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