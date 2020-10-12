import discord
import typing

from discord.ext import commands
from db import db_session, db_engine, Session


class Groups(commands.Cog, name='Groups'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['gruppenphase'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def groupphase(self, ctx, type:  typing.Optional[str]):
        if type:
            type = type.lower()

        if type == 'start':
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.green(),
                title=f'Die Gruppenphase wurde erfolgreich gestartet!'
            )

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)
        elif type == 'stop':
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.green(),
                title=f'Die Gruppenphase wurde erfolgreich beendet!'
            )

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'Bitte übergebe `start` oder `stop` als erstes Argument.'
            )

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Groups(bot))
