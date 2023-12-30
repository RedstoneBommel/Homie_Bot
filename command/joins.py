import json
import discord
import random
from discord.ext import commands

class joins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcomeMessages = [
            f"{member.mention} joined this server",
            f"{member.mention} welcome to this server",
            f"{member.mention} we hope you will have fun at this server",
            f"{member.mention} nice to meet you"
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
        await channel.send(welcomeMessage)
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
async def setup(bot):
    bot.add_cog(joins(bot))
