import discord
from discord.ext import commands
from discord import app_commands, Interaction

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

def check_link_youtube(link):
    if "youtube" in link:
        linkValid = True
    else:
        linkValid = False
    return linkValid
def check_link_twitch(link):
    if "twitch" in link:
        linkValid = True
    else:
        linkValid = False
    return linkValid

class webhook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    member = "Member"
    @app_commands.command(name = "webhook", description = "Create a webhook to get messages from youtube or twitch")
    @has_role(member)
    async def webhook(self, interaction: Interaction, platform: str, link: str):
        if platform == "YouTube" or "youtube" or "Youtube":
            if check_link_youtube(link):
                webhook = await interaction.channel.create_webhook(name = f"YouTube-WebHook for {interaction.user.id}")
                #await webhook.send("Hallo World!", name = "Youtube-Bot")
            await interaction.response.send_message("Please enter a valid link", ephemeral = True, delete_after = 20)
        elif platform == "Twitch" or "twitch":
            if check_link_twitch(link):
                webhook = await interaction.channel.create_webhook(name = f"Twitch-WebHook for {interaction.user.id}")
                #await webhook.send("Hallo World!", name = "Twitch-Bot")
            await interaction.response.send_message("Please enter a valid link", ephemeral = True, delete_after = 20)
        else:
            await interaction.response.send_message("Please enter a valid platform ( YouTube or Twitch )", ephemeral = True, delete_after = 20)
        
async def setup(bot):
    await bot.add_cog(webhook(bot))