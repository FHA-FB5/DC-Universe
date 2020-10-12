import discord
import typing

from discord.ext import commands
from db import db_session, db_engine, Session

from models.state import State


class Groups(commands.Cog, name='Groups'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['gruppenphase'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def groupphase(self, ctx, type:  typing.Optional[str]):
        if type:
            type = type.lower()

        if type == 'start':
            # check if grouphase is already startet
            state_groupphase_isStarted = State.get('groupphase_isStarted')
            if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es läuft schon eine Gruppenphase! Beende erst die alte, bevor du eine neue startest.'
                )

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

            else:
                # start groupphase
                State.set('groupphase_isStarted', str(True))

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'Die Gruppenphase wurde erfolgreich gestartet!'
                )

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
        elif type == 'stop':
            # check if grouphase is startet
            state_groupphase_isStarted = State.get('groupphase_isStarted')
            if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):

                # delete groupphase
                State.delete('groupphase_isStarted')

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
                    title=f'Es läuft keine Gruppenphase, die du beenden könntest!'
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
