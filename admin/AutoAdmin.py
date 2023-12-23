from datetime import datetime, timezone, timedelta
from discord import app_commands
from discord.ext import commands
import json
import discord
import os
import asyncio

class autoAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Automatic unmute
    def load_userData(filename):
        try:
            with open(filename, 'r') as admin_data:
                return json.load(admin_data)
        except FileNotFoundError:
            return None
    async def check_unmuteTime(users):
        while True:
            timeNow = datetime.now()
            for user in users:
                timeoutTime = datetime.fromisoformat(user["timeMuted"])
                memberId = user["id"]
                if timeNow >= timeoutTime:
                    interaction = discord.Interaction
                    permission = discord.PermissionOverwrite()
                    permission.speak = True
                    permission.send_messages = True
                    guild = interaction.guild
                    member = guild.get_member(memberId)
                    for channel in interaction.guild.channels:
                        if isinstance(channel, discord.VoiceChannel) or isinstance(channel, discord.TextChannel):
                            await channel.set_permissions(member, overwrite = permission)
                    filteredUsers = [user for user in users if user["id"] != memberId]
                    with open ("json/mute.json", "w") as admin_data:
                        json.dump(filteredUsers, admin_data)
            await asyncio.sleep(60)
    if __name__ == "__main__":
        users = load_userData("json/mute.json")
        asyncio.run(check_unmuteTime(users))

async def setup(bot):
    await bot.add_cog(autoAdmin(bot))