import discord
from random import randint

from discord.ext import commands


class Fun(commands.Cog, name='Fun'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.caroMember = None

    @commands.command(aliases=['keks'], hidden=True)
    async def cookie(self, ctx, member: discord.Member):
        if ctx.author.id == member.id:
            await ctx.send('{0.mention} zu Eigenlob sage ich nur: https://tenor.com/view/shame-sad-too-bad-hot-fuzz-nick-gif-4991655'.format(member))
        elif self._last_member is None or self._last_member.id != member.id:
            await ctx.send('{0.mention} hier ist ein Keks für dich 🍪'.format(member))
        else:
            await ctx.send('Ach {0.mention}... {1.mention} bekam zuletzt einen Keks.'.format(ctx.author, member))
        self._last_member = member

    @commands.command(hidden=True)
    async def ping(self, ctx):
        await ctx.send('{0.mention} pong!'.format(ctx.author))

    @commands.command(hidden=True)
    async def pong(self, ctx):
        await ctx.send('{0.mention} ping'.format(ctx.author))

    @commands.command(aliases=['kuchen'], hidden=True)
    async def cake(self, ctx):
        await ctx.send('{0.mention} The Cake Is A Lie'.format(ctx.author))

    @commands.command(hidden=True)
    async def alive(self, ctx):
        await ctx.send('{0.mention} https://www.youtube.com/watch?v=Y6ljFaKRTrI'.format(ctx.author))

    @commands.command(aliases=['münzwurf', 'münze', 'kopf', 'zahl', 'coin'], hidden=True)
    async def coinflip(self, ctx):
        coin = randint(0, 1)
        if coin == 0:
            await ctx.send('{0.mention} Kopf'.format(ctx.author))
        else:
            await ctx.send('{0.mention} Zahl'.format(ctx.author))

    @commands.command(aliases=['tableflip'], hidden=True)
    async def flip(self, ctx):
        await ctx.send('{0.mention} (╯°□°）╯︵ ┻━┻'.format(ctx.author))

    @commands.command(aliases=['mayo'], hidden=True)
    async def mayonaise(self, ctx):
        await ctx.send('{0.mention} https://www.youtube.com/watch?v=hVtSkF-hBXE'.format(ctx.author))

    @commands.command(aliases=['carlo'], hidden=True)
    async def caro(self, ctx):
        ping = ctx.author
        if self.caroMember == None:
            tmp = ctx.guild.get_member(163444674097446913)
            if tmp:
                self.caroMember = tmp

        if self.caroMember:
            ping = self.caroMember
        await ctx.send('{0.mention} https://youtu.be/NFAjjdM0HaU?t=27'.format(ping))

    @commands.command(hidden=True)
    async def hoever(self, ctx):
        await ctx.send('{0.mention} https://soundcloud.com/cvrofficial/hoever/s-eXVFz'.format(ctx.author))

    @commands.command(hidden=True)
    async def matheisttoll(self, ctx):
        await ctx.send('{0.mention} Mathe ist magic!'.format(ctx.author))

    @commands.command(hidden=True)
    async def matheistmagic(self, ctx):
        await ctx.send('{0.mention} Und wie Sie sehen, es funktioniert auf magische Weise. Magic Mathe!'.format(ctx.author))

    @commands.command(hidden=True)
    async def error(self, ctx):
        await ctx.send('{0.mention} Claßen: Error heißt ich weigere mich!'.format(ctx.author))

    @commands.command(hidden=True)
    async def spam(self, ctx):
        await ctx.send('{0.mention} selber Spam!'.format(ctx.author))


def setup(bot):
    bot.add_cog(Fun(bot))
