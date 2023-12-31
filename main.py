from command import help, info, funny, games, joins, translation
from admin import AdminCommand, AutoAdmin, roles
from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
import json
import random

class HomieBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(command_prefix = "!", intents = intents)
    async def on_ready(self):
        print("load extensions")
        await self.load_extension('admin.AdminCommand')
        await self.load_extension('admin.AutoAdmin')
        await self.load_extension('admin.roles')
        await self.load_extension('command.help')
        await self.load_extension('command.info')
        # await self.load_extension('command.funny')
        # await self.load_extension('command.games')
        # await self.load_extension('command.joins')
        await self.load_extension('command.translation')
        print("sync extensions")
        await self.tree.sync()
        print("Bot is ready")
    async def on_message(self, message):
        if message.author == self.user:
            return
        messageWords = message.content.split()
        with open('json/bannedWords.json', 'r') as admin_data:
            bannedWords = json.load(admin_data)
        bannedWords = bannedWords['bannedWords']
        for i in messageWords:
            if i in bannedWords:
                await message.author.send(f"Please don't use this word: {i}")
                with open('json/member.json', 'r') as admin_data:
                    memberJSON = json.load(admin_data)
                guild = message.guild
                discord_member = await guild.fetch_member(message.author.id)
                if message.author.name in memberJSON:
                    print(f"bannedWord used by {message.author.name}")
                    if message.author.id == 1060970436827025502:
                        return "It was just the Cheffe"
                    else:
                        memberJSON[message.author.name]['bannedWordsCounter'] += 1
                        maxValue = 3
                        kickValue = 5
                        if memberJSON[message.author.name]['bannedWordsCounter'] == maxValue:
                            await discord_member.send("You used the banned words three times, two times more and you will be banned.")
                        elif memberJSON[message.author.name]['bannedWordsCounter'] == kickValue:
                            await discord_member.send("You used the banned words five times, now you are kicked.")
                            await guild.kick(discord_member)
                else:
                    memberJSON[message.author.name] = {"bannedWordsCounter": 1}
                with open('json/member.json', 'w') as admin_data:
                    json.dump(memberJSON, admin_data)
    async def on_member_join(self, member):
        if not member.bot:
            welcomeMessages = [
                "joined this server",
                "welcome to this server",
                "we hope you will have fun at this server",
                "nice to meet you"
            ]
            welcomeMessage = random.choice(welcomeMessages)
            with open("json/admin.json", "r") as admin_data:
                admin_data = json.load(admin_data)
                for channel in member.guild.channels:
                    if channel.id == admin_data["joins"]:
                        break
                else:
                    print("No Join Channel found")
                    return
                for rule in member.guild.channels:
                    if rule.id == admin_data["rules"]:
                        await channel.send(member.name + welcomeMessage + f" \n Check out our Server Rules: {rule.id.mention}")
                    await channel.send(member.name + welcomeMessage)
            with open("json/member.json", "r+") as member_data:
                member_data = json.load(member_data)
                if member.name in member_data:
                    member_data.close()
                    return "Member is already in the register"
                else:
                    member_data[member.name] = {"name": member.name, "id": member.id, "roles": [role.name for role in member.roles], "bannedWordsCounter": 0}
                    json.dump(member_data, member_data)
                    member_data.close()
            await member.send("Check out our rule channel to be able to our server rules")
load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.all()
HomieBot = HomieBot(intents = intents)
HomieBot.run(token)