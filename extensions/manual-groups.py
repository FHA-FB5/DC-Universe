import discord
import os

from discord.ext import commands


class Groups(commands.Cog, name='Groups'):
    def __init__(self, bot):
        self.bot = bot

        


def setup(bot):
    bot.add_cog(Groups(bot))
