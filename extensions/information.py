import discord
import os
import typing

class Information(commands.Cog, name='Informations'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['services'], hidden=True)
    async def shortMentionForServices(self, ctx, active: typing.Optional[str]):
        


def setup(bot):
    bot.add_cog(Information(bot))
