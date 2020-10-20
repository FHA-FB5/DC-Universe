import discord
import os
import typing

from discord.ext import commands


class ManualGroups(commands.Cog, name='ManualGroups'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['poll', 'p'], hidden=True)
    async def createPoll(self, ctx, msg: typing.Optional[str]):
        if not msg:
            embed = discord.Embed (
                colour = discord.Colour.red(),
                title = f'Bitte gib eine Frage oder eine Nachricht an, worüber abgestimmt werden kann!'
            )
            await ctx.send(ctx.author.mention, embed=embed)
            return

        else:
            embed = discord.Embed (
                colour = discord.Colour.blue(),
                title = f'Umfrage:',
                description = msg,
                footer = "Stimmt jetzt über die verfügbaren Reaktionen ab."
            )

            await ctx.send(ctx.channel.mention, embed=embed)
            return