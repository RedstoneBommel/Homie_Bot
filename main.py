from command import CommandsCommand, help, info, funny, games, joins
from admin import AdminCommand, AutoAdmin, roles, log
from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
import json

class HomieBot(commands.Bot):

    def __init__(self, intents):
        super().__init__(command_prefix = "!", intents = intents)
    
    async def on_ready(self):
        await self.load_extension('admin.AdminCommand')
        await self.load_extension('admin.AutoAdmin')
        # await self.load_extension('admin.roles')
        # await self.load_extension('admin.log')

        # await self.load_extension('command.CommandsCommand')
        # await self.load_extension('command.help')
        # await self.load_extension('command.info')
        # await self.load_extension('command.funny')
        # await self.load_extension('command.games')
        # await self.load_extension('command.joins')

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
                if message.author.name in memberJSON:
                    print("check")
                    memberJSON[message.author.name]['bannedWordsCounter'] += 1
                else:
                    memberJSON[message.author.name] = {"bannedWordsCounter": 1}
                with open('json/member.json', 'w') as admin_data:
                    json.dump(memberJSON, admin_data)

        
load_dotenv()

token = os.getenv('TOKEN')
intents = discord.Intents.all()
HomieBot = HomieBot(intents = intents)
HomieBot.run(token)