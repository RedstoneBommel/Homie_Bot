import discord
from discord import Interaction, Embed, app_commands, ButtonStyle, Color, File
from discord.ui import View, Button
from discord.ext import commands
import random
import json
import asyncio

def has_role(role_name):
    def predicate(interaction: Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class flagguesser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.correct = 0
        self.incorrect = 0
    member = "Member"
    @app_commands.command(name = "flagguesser", description = "Do you know every country and there flag?")
    @has_role(member)
    async def flagguesser(self, interaction: Interaction, rounds: int = None):
        def setOption(list):
            i = random.randint(0, len(list) - 1)
            j = list[i]
            del list[i]
            return j
        if rounds == None:
            rounds = 10
        elif rounds > 194:
            rounds = 194
        with open("json/scoreboard.json", "r+") as scoreboard:
            scoreboardData = json.load(scoreboard)
        if interaction.user.name in scoreboardData["flagGuesser"]:
            print(f"{interaction.user.name} already played FlagGuesser")
        else:
            scoreboardData["flagGuesser"][interaction.user.name] = {
                "topScore": 0
            }
            json.dump(scoreboardData, scoreboard)
        with open("json/flagGuesser.json", "r") as flag_json:
            flagGuesserData = json.load(flag_json)
        country = [flagGuesserData[country]["land"] for country in flagGuesserData]
        iso = [flagGuesserData[country]["iso 3166 alpha-2"] for country in flagGuesserData]
        path = [flagGuesserData[country]["flag"] for country in flagGuesserData]
        if len(country) == len(iso) == len(path) and len(country) == 193:
            event = asyncio.Event()
            for i in range(rounds):
                roundFlag = random.randint(0, 192)
                isoCode = iso[roundFlag]
                pathChoice = path[roundFlag]
                options = [country[roundFlag]]
                for j in range(0, 3):
                    randomOption = random.randint(0, 192)
                    while country[randomOption] in options:
                        randomOption = random.randint(0, 192)
                    options.append(country[randomOption])
                flagImage = File(f"{pathChoice}", filename = f"{isoCode.lower()}.png")
                guesser = Embed(title = "Flag Guesser - Do you know this country?")
                guesser.color = Color.from_rgb(0, 255, 0)
                guesser.set_image(url = f"attachment://{isoCode.lower()}.png")
                guesser.set_footer(text = "Game developed by RedstoneBommel")
                optionMenu = View()
                button1 = Button(label = setOption(options), style = ButtonStyle.blurple)
                button2 = Button(label = setOption(options), style = ButtonStyle.blurple)
                button3 = Button(label = setOption(options), style = ButtonStyle.blurple)
                button4 = Button(label = setOption(options), style = ButtonStyle.blurple)
                async def button_callback_button1(interaction):
                    with open("json/scoreboard.json", "r") as flag_score:
                        flagGuesserData = json.load(flag_score)
                    text = button1.label
                    control = True
                    counter = 0
                    while control:
                        for i in country:
                            if i == text:
                                control = False
                                break
                            counter += 1
                        if counter != 0:
                            pathCorrect = path[counter]
                            if pathCorrect == pathChoice:
                                if interaction.user.name in flagGuesserData["flagGuesser"]:
                                    flagGuesserData["flagGuesser"][interaction.user.name]["topScore"] += 1
                                    self.correct += 1
                                    event.set()
                                    await interaction.response.send_message("Correct Answer!", delete_after = 5, ephemeral = True)
                                else:
                                    return await interaction.response.send_message("Couldn't find your top score! We couldn't save your answer!")
                            else:
                                if interaction.user.name in flagGuesserData["flagGuesser"]:
                                    flagGuesserData["flagGuesser"][interaction.user.name]["topScore"] -= 1
                                    self.incorrect += 1
                                    event.set()
                                    await interaction.response.send_message("Wrong Answer!", delete_after = 5, ephemeral = True)
                                else:
                                    return await interaction.response.send_message("Couldn't find your top score! We couldn't save your answer!")
                        else:
                            return await interaction.response.send_message("Problems while loading results! Please try again later.")
                    with open("json/scoreboard.json", "w") as flag_score:
                        json.dump(flagGuesserData, flag_score)
                async def button_callback_button2(interaction):
                    with open("json/scoreboard.json", "r") as flag_score:
                        flagGuesserData = json.load(flag_score)
                    text = button2.label
                    control = True
                    counter = 0
                    while control:
                        for i in country:
                            if i == text:
                                control = False
                                break
                            counter += 1
                        if counter != 0:
                            pathCorrect = path[counter]
                            if pathCorrect == pathChoice:
                                if interaction.user.name in flagGuesserData["flagGuesser"]:
                                    flagGuesserData["flagGuesser"][interaction.user.name]["topScore"] += 1
                                    self.correct += 1
                                    event.set()
                                    await interaction.response.send_message("Correct Answer!", delete_after = 5, ephemeral = True)
                                else:
                                    return await interaction.response.send_message("Couldn't find your top score! We couldn't save your answer!")
                            else:
                                if interaction.user.name in flagGuesserData["flagGuesser"]:
                                    flagGuesserData["flagGuesser"][interaction.user.name]["topScore"] -= 1
                                    self.incorrect += 1
                                    event.set()
                                    await interaction.response.send_message("Wrong Answer!", delete_after = 5, ephemeral = True)
                                else:
                                    return await interaction.response.send_message("Couldn't find your top score! We couldn't save your answer!")
                        else:
                            return await interaction.response.send_message("Problems while loading results! Please try again later.")
                    with open("json/scoreboard.json", "w") as flag_score:
                        json.dump(flagGuesserData, flag_score)
                async def button_callback_button3(interaction):
                    with open("json/scoreboard.json", "r") as flag_score:
                        flagGuesserData = json.load(flag_score)
                    text = button3.label
                    control = True
                    counter = 0
                    while control:
                        for i in country:
                            if i == text:
                                control = False
                                break
                            counter += 1
                        if counter != 0:
                            pathCorrect = path[counter]
                            if pathCorrect == pathChoice:
                                if interaction.user.name in flagGuesserData["flagGuesser"]:
                                    flagGuesserData["flagGuesser"][interaction.user.name]["topScore"] += 1
                                    self.correct += 1
                                    event.set()
                                    await interaction.response.send_message("Correct Answer!", delete_after = 5, ephemeral = True)
                                else:
                                    return await interaction.response.send_message("Couldn't find your top score! We couldn't save your answer!")
                            else:
                                if interaction.user.name in flagGuesserData["flagGuesser"]:
                                    flagGuesserData["flagGuesser"][interaction.user.name]["topScore"] -= 1
                                    self.incorrect += 1
                                    event.set()
                                    await interaction.response.send_message("Wrong Answer!", delete_after = 5, ephemeral = True)
                                else:
                                    return await interaction.response.send_message("Couldn't find your top score! We couldn't save your answer!")
                        else:
                            return await interaction.response.send_message("Problems while loading results! Please try again later.")
                    with open("json/scoreboard.json", "w") as flag_score:
                        json.dump(flagGuesserData, flag_score)
                async def button_callback_button4(interaction):
                    with open("json/scoreboard.json", "r") as flag_score:
                        flagGuesserData = json.load(flag_score)
                    text = button4.label
                    control = True
                    counter = 0
                    while control:
                        for i in country:
                            if i == text:
                                control = False
                                break
                            counter += 1
                        if counter != 0:
                            pathCorrect = path[counter]
                            if pathCorrect == pathChoice:
                                if interaction.user.name in flagGuesserData["flagGuesser"]:
                                    flagGuesserData["flagGuesser"][interaction.user.name]["topScore"] += 1
                                    self.correct += 1
                                    event.set()
                                    await interaction.response.send_message("Correct Answer!", delete_after = 5, ephemeral = True)
                                else:
                                    return await interaction.response.send_message("Couldn't find your top score! We couldn't save your answer!")
                            else:
                                if interaction.user.name in flagGuesserData["flagGuesser"]:
                                    flagGuesserData["flagGuesser"][interaction.user.name]["topScore"] -= 1
                                    self.incorrect += 1
                                    event.set()
                                    await interaction.response.send_message("Wrong Answer!", delete_after = 5, ephemeral = True)
                                else:
                                    return await interaction.response.send_message("Couldn't find your top score! We couldn't save your answer!")
                        else:
                            return await interaction.response.send_message("Problems while loading results! Please try again later.")
                    with open("json/scoreboard.json", "w") as flag_score:
                        json.dump(flagGuesserData, flag_score)
                button1.callback = button_callback_button1
                button2.callback = button_callback_button2
                button3.callback = button_callback_button3
                button4.callback = button_callback_button4
                optionMenu.add_item(button1)
                optionMenu.add_item(button2)
                optionMenu.add_item(button3)
                optionMenu.add_item(button4)
                if i != 0:
                    async def delete_after_delay(delay, message):
                        await asyncio.sleep(delay)
                        await message.delete()
                    ephemeral_message = await interaction.followup.send(embed = guesser, view = optionMenu, file = flagImage, ephemeral = True)
                    asyncio.create_task(delete_after_delay(60, ephemeral_message))
                else:
                    await interaction.response.send_message(embed = guesser, view = optionMenu, file = flagImage, ephemeral = True, delete_after = 60)
                while not event.is_set():
                    await event.wait()
                event.clear()
            await interaction.followup.send(f"{interaction.user.mention}, you had {self.correct} correct answers and {self.incorrect} incorrect answers!", ephemeral = True)
        else:
            print("Error: Couldn't load needed data for Flag Guesser.")
    
    @app_commands.command(name = "scoreboard", description = "See the best player in Flag Guesser")
    @has_role(member)
    async def scoreboard(self, interaction: Interaction):
        with open("json/scoreboard.json", "r") as scoreboard:
            scoreboardData = json.load(scoreboard)
        value = 0
        bestFiveScores = []
        bestFiveScoreMembers = []
        playedScores = []
        playedMembers = []
        playedScoresSorted = []
        playedMembersSorted = []
        for i in scoreboardData["flagGuesser"]:
            playedMembers.append(i)
            playedScores.append(scoreboardData["flagGuesser"][i]["topScore"])
        while len(playedScores) > 0:
            i = playedScores[0]
            for j in playedScores:
                if j > i:
                    i = j
            counter = 0
            for x in playedScores:
                if x == i:
                    break
                counter += 1
            playedScoresSorted.append(i)
            playedMembersSorted.append(playedMembers[counter])
            playedScores.remove(i)
            playedMembers.remove(playedMembers[counter])
        if len(playedScoresSorted) >= 5:
            for i in range(0, 5):
                bestFiveScores.append(playedScoresSorted[value])
                bestFiveScoreMembers.append(playedMembersSorted[value])
                value += 1
            scoreboard = Embed(title = "List of the five best scores at this server")
            scoreboard.color = Color.from_rgb(207, 166, 61)
            scoreboard.add_field(name = "**First Place:**", value = f"**{bestFiveScoreMembers[0]}** with **{str(bestFiveScores[0])}** points", inline = False)
            scoreboard.add_field(name = "**Second Place:**", value = f"**{bestFiveScoreMembers[1]}** with **{str(bestFiveScores[1])}** points", inline = False)
            scoreboard.add_field(name = "**Third Place:**", value = f"**{bestFiveScoreMembers[2]}** with **{str(bestFiveScores[2])}** points", inline = False)
            scoreboard.add_field(name = "**Fourth Place:**", value = f"**{bestFiveScoreMembers[3]}** with **{str(bestFiveScores[3])}** points", inline = False)
            scoreboard.add_field(name = "**Fifth Place:**", value = f"**{bestFiveScoreMembers[4]}** with **{str(bestFiveScores[4])}** points", inline = False)
            scoreboard.set_footer(text = "Score Board generated by Homie")
            await interaction.response.send_message(embed = scoreboard)
        else:
            await interaction.response.send_message("More Players needed for this Scoreboard")

async def setup(bot):
    await bot.add_cog(flagguesser(bot))