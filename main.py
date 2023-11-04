from command import CommandsCommand, help, info, funny, games, joins
from admin import AdminCommand, roles, log
from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

class HomieBot(commands.Bot):

    def __init__(self, intents):
        super().__init__(command_prefix = "!", intents = intents)
    
    async def on_ready(self):
        # await self.load_extension('admin.AdminCommand')
        # await self.load_extension('admin.roles')
        # await self.load_extension('admin.log')

        # await self.load_extension('command.CommandsCommand')
        # await self.load_extension('command.help')
        # await self.load_extension('command.info')
        # await self.load_extension('command.funny')
        # await self.load_extension('command.games')
        # await self.load_extension('command.joins')

        # await self.tree.sync()

        print("Bot is ready")
    
    async def on_message(self, message):

        if message.author == self.user:
            return
        
load_dotenv()

token = os.getenv('TOKEN')
intents = discord.Intents.all()
HomieBot = HomieBot(intents = intents)
HomieBot.run(token)