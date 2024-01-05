from command import help, info, funny, translation, flagGuesser, dragonDuel
from admin import AdminCommand, AutoAdmin, roles, tickets
from auto import twitch, youtube
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
        await self.load_extension('admin.tickets')
        await self.load_extension('command.help')
        await self.load_extension('command.info')
        # await self.load_extension('command.funny')
        # await self.load_extension('command.flagGuesser')
        # await self.load_extension('command.dragonDuel')
        await self.load_extension('command.translation')
        # await self.load_extension('auto.twitch')
        # await self.load_extension('auto.youtube')
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
        guild = member.guild
        welcomeMessages = [
            "joined this server",
            "welcome to this server",
            "we hope you will have fun at this server",
            "nice to meet you"
        ]
        welcomeMessage = random.choice(welcomeMessages)
        with open("json/admin.json", "r") as admin_data:
            admin_data = json.load(admin_data)
            for channel in guild.channels:
                print(channel.id)
                if channel.id == admin_data["joins"]:
                    break
            else:
                print("No Join Channel found")
                return
            for rule in guild.channels:
                if rule.id == admin_data["rules"]:
                    await channel.send(f"{member.mention} {welcomeMessage} \n Check out our Server Rules: {rule.mention}")
                    break
            else:
                await channel.send(member.mention + welcomeMessage)
                return
        with open("json/member.json", "r+") as memberData:
            member_data = json.load(memberData)
            if member.name in member_data:
                return "Member is already in the register"
            else:
                member_data[member.name] = {"name": member.name, "id": member.id, "roles": [], "bannedWordsCounter": 0}
                memberData.seek(0)
                json.dump(member_data, memberData)
load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.all()
HomieBot = HomieBot(intents = intents)
HomieBot.run(token)