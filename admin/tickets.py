import discord
from discord import app_commands, Interaction, Embed, Color, ButtonStyle, PermissionOverwrite
from discord.ext import commands
from discord.ui import Modal, View, Button

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class Ticket(Modal):
        def __init__(self):
            super().__init__(title = "Generate a ticket")
        topic = discord.ui.TextInput(label = "Your problem", style = discord.TextStyle.short, required = True, max_length = 30)
        message = discord.ui.TextInput(label = "Explain your problem closer", style = discord.TextStyle.long, required = True, max_length = 2000)
        importanceLevel = discord.ui.TextInput(label = "How important is your problem?", style = discord.TextStyle.short, placeholder = "Important/Unimportant", required = True, max_length = 11)
        async def on_submit(self, interaction: Interaction):
            memberID = interaction.user.id
            await interaction.response.send_message(f"Thanks for your ticket {interaction.user.mention}. One of our moderators will help you soon!", ephemeral = True, delete_after = 60)
            ticketCard = Embed(title = self.topic.value)
            ticketCard.color = Color.from_rgb(255, 255, 0)
            ticketCard.set_thumbnail(url = interaction.user.display_avatar.url)
            ticketCard.description = self.message.value
            ticketCard.add_field(name = "Importance Level: ", value = self.importanceLevel.value, inline = False)
            ticketCard.set_footer(text = f"Ticket generated by {interaction.user.id}({interaction.user.name}), sended by Homie")
            ticketChannel = discord.utils.get(interaction.guild.text_channels, id = 1191759336930816050)
            close = Button(label = "Close Ticket", style = ButtonStyle.red)
            start = Button(label = "Start Ticket", style = ButtonStyle.green)
            async def button_callback_close(interaction):
                await interaction.message.delete()
                ticketChannel = discord.utils.get(interaction.guild.text_channels, name = f"ticket-for-{memberID}")
                if ticketChannel != None:
                    await ticketChannel.delete()
                else:
                    print(f"Could not find channel: ticket-for-{memberID}")
            async def button_callback_start(interaction):
                overwrites = {
                    interaction.guild.default_role: PermissionOverwrite(read_messages=False),
                    interaction.user: PermissionOverwrite(read_messages=True)
                }
                await interaction.response.send_message("Channel is ready", delete_after = 5)
                channel_name = "ticket-for-" + str(memberID)
                await interaction.guild.create_text_channel(channel_name, overwrites=overwrites)
            close.callback = button_callback_close
            start.callback = button_callback_start
            buttonUI = View()
            buttonUI.add_item(close)
            buttonUI.add_item(start)
            await ticketChannel.send(embed = ticketCard, view = buttonUI)

class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    everyone = "@everyone"
    @app_commands.command(name = "ticket", description = "Generate a new ticket, to get specific support")
    @has_role(everyone)
    async def ticket(self, interaction: Interaction):
        await interaction.response.send_modal(Ticket())

async def setup(bot):
    await bot.add_cog(tickets(bot))