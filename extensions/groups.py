import discord

from discord.ext import commands
from db import db_session, db_engine, Session


class Groups(commands.Cog, name='Groups'):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Groups(bot))
