from discord import app_commands, Button, ButtonStyle, Interaction, Embed
from discord.ext import commands
import discord

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    class HelpButton(Button):
        def __init__(self, label, command):
            super().__init__(style=ButtonStyle.primary, label=label)
            self.command = command
        async def callback(self, interaction: Interaction):
            await interaction.response.send_message(f"Der Befehl `{self.command}` macht folgendes: ...")
    everyone = "@everyone"
    @app_commands.command(name = "help", description = "Get a explanation of all commands")
    @has_role(everyone)
    async def help(self, interaction: Interaction):
        embed = Embed(title = "Help", description = "Show help for all commands:")
        buttons = [
            Button("/info", "info"),
            Button("/translate", "translate"),
            Button("/rules", "rules"),
        ]
        await interaction.response.send_message(embed = embed, buttons = buttons)
async def setup(bot):
    await bot.add_cog(help(bot))