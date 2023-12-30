from discord import app_commands, Interaction, ButtonStyle, Embed, Color
from discord.ext import commands
import discord
from discord.ui import Button, View

def has_role(role_name):
    def predicate(interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    everyone = "@everyone"
    # Help for all commands
    @app_commands.command(name = "help", description = "Get a explanation of all commands")
    @has_role(everyone)
    async def help(self, interaction: Interaction):
        info = Button(label = "/info", style = ButtonStyle.blurple)
        rules = Button(label = "/rules", style = ButtonStyle.blurple)
        translate = Button(label = "/translate", style = ButtonStyle.blurple)
        async def button_callback_info(interaction):
            info = Embed(title = "Info Command")
            info.color = Color.from_rgb(255, 0, 0)
            info.add_field(name = "Basic Command:", value = "**`/info`** \n This Command will show you general information about your self")
            info.add_field(name = "Specific Command", value = "**`/info <username>`** \n This Command will show your general information about about this user")
            info.set_footer(text = "This embed was created by Homie")
            await interaction.response.send_message(embed = info, ephemeral=True, delete_after = 15)
        async def button_callback_rules(interaction):
            rules = Embed(title = "Rules Command")
            rules.color = Color.from_rgb(255, 0, 0)
            rules.add_field(name = "Command:", value = "**`/rules`** \n This Command will show you in which channel you could find the server rules")
            rules.set_footer(text = "This embed was created by Homie")
            await interaction.response.send_message(embed = rules, ephemeral=True, delete_after = 15)
        async def button_callback_translate(interaction):
            translate = Embed(title = "Translate Command")
            translate.color = Color.from_rgb(255, 0, 0)
            translate.add_field(name = "Basic Command:", value = "**`/translate <text>`** \n This Command will translate any text for into English")
            translate.add_field(name = "Specific Command", value = "**`/translate <text> <language>`** \n This Command will translate any text into the language you choose")
            translate.set_footer(text = "This embed was created by Homie")
            await interaction.response.send_message(embed = translate, ephemeral=True, delete_after = 15)
        info.callback = button_callback_info
        rules.callback = button_callback_rules
        translate.callback = button_callback_translate
        view = View()
        view.add_item(info)
        view.add_item(rules)
        view.add_item(translate)
        help = Embed(title = "Help")
        help.color = Color.from_rgb(255, 0, 0)
        help.add_field(name = "All Commands for Members", value = "Please use all commands carefully and don't spam unnecessarily in the chat")
        help.set_footer(text = "This embed was created by Homie")
        await interaction.response.send_message(embed = help, view = view, ephemeral=True, delete_after = 60)
    # Information about Homie
    @app_commands.command(name = "homie", description = "Who is Homie?")
    @has_role(everyone)
    async def homie(self, interaction: Interaction):
        githubLink = Button(label = "GitHub", url = "https://github.com/RedstoneBommel/Homie_Bot")
        github = View()
        github.add_item(githubLink)
        homie = Embed(title = "Who is Homie?")
        homie.color = Color.from_rgb(0, 0, 255)
        homie.add_field(name = "Homie (Discord Bot)", value = "Homie is a Discord bot created by RedstoneBommel to keep order and entertainment on Discord servers \n If you want more information you could check out RedstoneBommels GitHub")
        await interaction.response.send_message(embed = homie, view = github)


async def setup(bot):
    await bot.add_cog(help(bot))