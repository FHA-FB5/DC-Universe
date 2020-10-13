import discord
import os

from discord.ext import commands


class groups(commands.Cog, name='Groups'):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Members(bot))
