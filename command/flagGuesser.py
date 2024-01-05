import discord
from discord import Interaction, Embed, app_commands, ButtonStyle, Color
from discord.ui import View, Button
from discord.ext import commands
import random
import json

def has_role(role_name):
    def predicate(interaction: Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class flagguesser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    member = "Member"
    @app_commands.command(name = "flagguesser", description = "Do you know every country and there flag?")
    @has_role(member)
    async def flagguesser(self, interaction: Interaction, rounds: int = None):
        def setOption(list):
            i = random.randint(0, len(list))
            j = list[i]
            del list[i]
            return j
        if rounds == None:
            rounds = 10
        elif rounds > 195:
            rounds = 195
        with open("json/flagGuesser.json", "r") as flag_json:
            flagGuesserData = json.load(flag_json)
        country = [flagGuesserData[country]["land"] for country in flagGuesserData]
        iso = [flagGuesserData[country]["iso 3166 alpha-2"] for country in flagGuesserData]
        path = [flagGuesserData[country]["flag"] for country in flagGuesserData]
        if len(country) == len(iso) == len(path) and len(country) != 0:
            for i in rounds:
                roundFlag = random.randint(0, 195)
                pathChoice = [path[roundFlag]]
                options = [country[roundFlag]]
                for i in range(0, 3):
                    randomOption = random.randint(0, 195)
                    while country[randomOption] in options:
                        randomOption = random.randint(0, 195)
                    options.append(country[randomOption])
                guesser = Embed(title = "Flag Guesser")
                guesser.color = Color.from_rgb(0, 255, 0)
                guesser.add_field(name = "What is the name of this country?", value = pathChoice)
                guesser.set_footer(text = "Game developed by RedstoneBommel")
                optionMenu = View()
                button1 = Button(text = setOption(options))
                button2 = Button(text = setOption(options))
                button3 = Button(text = setOption(options))
                button4 = Button(text = setOption(options))
                async def button_callback_button(interaction):
                    print("Klappt")
                button1.callback = button_callback_button
                button2.callback = button_callback_button
                button3.callback = button_callback_button
                button4.callback = button_callback_button
                optionMenu.add_item(button1)
                optionMenu.add_item(button2)
                optionMenu.add_item(button3)
                optionMenu.add_item(button4)
            await interaction.response.send_message(embed = guesser, view = optionMenu, ephemeral = True)
        else:
            print("Error: Couldn't load needed data for Flag Guesser.")
            return await interaction.response.send_message("Problem while loading data. Retry later again")

async def setup(bot):
    await bot.add_cog(flagguesser(bot))