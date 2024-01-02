import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Modal
from discord import Interaction, Embed, Color

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class Ticket(Modal):
        def __init__(self):
            super().__init__(title = "Generate a ticket")
        topic = discord.ui.TextInput(label = "Your problem", style = discord.TextStyle.short, required = True, max_length = 100)
        message = discord.ui.TextInput(label = "Explain your problem closer", style = discord.TextStyle.long, required = True, max_length = 2000)
        importanceLevel = discord.ui.TextInput(label = "How important is your problem?", style = discord.TextStyle.short, placeholder = "Important/Uninportant", required = True, max_length = 11)
        async def on_submit(self, interaction: Interaction):
            ticketCard = Embed(title = self.topic.value)
            ticketCard.color = Color.from_rgb(255, 255, 0)
            ticketCard.set_thumbnail(url = interaction.user.display_avatar.url)
            ticketCard.description = self.message.value
            ticketCard.add_field(name = "Importance Level: ", value = self.importanceLevel.value, inline = False)
            await interaction.response.send_message(f"Thanks for your ticket {interaction.user.mention}. One of our moderators will help you soon!", ephemeral = True)
            ticketChannel = discord.utils.get(interaction.guild.text_channels, id = 1191759336930816050)
            await ticketChannel.send(embed = ticketCard)

class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    adminRole = "Cheffe"
    member = "Member"
    everyone = "@everyone"
    @app_commands.command(name = "ticket", description = "Generate a new ticket, to get specific support")
    @has_role(everyone)
    async def ticket(self, interaction: Interaction):
        await interaction.response.send_modal(Ticket())

async def setup(bot):
    await bot.add_cog(tickets(bot))