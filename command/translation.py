from googletrans import Translator
from discord import app_commands
from discord.ext import commands
from discord import Interaction
import discord
import googletrans

def has_role(role_name):
    def predicate(interaction: Interaction):
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        return role is not None
    return commands.check(predicate)

class translation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
    everyone = "@everyone"
    @app_commands.command(name = "translate", description = "Translate messages to a specific language")
    @has_role(everyone)
    async def translate(self, interaction: Interaction, text: str, language: str = None):
        default_language = "en"
        if language is None:
            language = default_language
        src_language = self.translator.detect(text).lang
        if src_language not in googletrans.LANGUAGES or language not in googletrans.LANGUAGES:
            await interaction.response.send_message("Unknown language")
            return "Unknown language"
        else:
            # Aufschieben der Interaktion
            await interaction.response.defer()
            # Senden der Nachfolgenachricht
            translated_text = self.translator.translate(text, src = src_language, dest = language).text
            await interaction.followup.send(translated_text)



async def setup(bot):
    await bot.add_cog(translation(bot))