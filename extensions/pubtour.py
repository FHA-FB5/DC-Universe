import discord
import os
import typing

from discord.ext import commands


class Pubtour(commands.Cog, name='Pubtour'):
    def __init__(self, bot):
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance(self.bot_user_id, str):
            self.bot_user_id = int(self.bot_user_id)

    @commands.command(aliases=['phase2'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def kneipentour(self, ctx, *channel: discord.VoiceChannel ):
        name_prefix = 'Kneipentour-'


def setup(bot):
    bot.add_cog(Pubtour(bot))