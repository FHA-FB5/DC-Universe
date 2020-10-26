import discord
import typing

from random import randint

from discord.ext import commands


class Fun(commands.Cog, name='Fun'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.caroMember = None

    @commands.command(aliases=['keks'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def cookie(self, ctx, member: discord.Member):
        if ctx.author.id == member.id:
            await ctx.send('{0.mention} zu Eigenlob sage ich nur: https://tenor.com/view/shame-sad-too-bad-hot-fuzz-nick-gif-4991655'.format(member))
        elif self._last_member is None or self._last_member.id != member.id:
            await ctx.send('{0.mention} hier ist ein Keks für dich 🍪'.format(member))
        else:
            await ctx.send('Ach {0.mention}... {1.mention} bekam zuletzt einen Keks.'.format(ctx.author, member))
        self._last_member = member

    @commands.command(hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send('{0.mention} pong!'.format(ctx.author))

    @commands.command(hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def pong(self, ctx):
        await ctx.send('{0.mention} ping'.format(ctx.author))

    @commands.command(aliases=['kuchen'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def cake(self, ctx):
        await ctx.send('{0.mention} The Cake Is A Lie'.format(ctx.author))

    @commands.command(hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def alive(self, ctx):
        await ctx.send('{0.mention} https://www.youtube.com/watch?v=Y6ljFaKRTrI'.format(ctx.author))

    @commands.command(aliases=['münzwurf', 'münze', 'kopf', 'zahl', 'coin'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def coinflip(self, ctx):
        coin = randint(0, 1)
        if coin == 0:
            await ctx.send('{0.mention} Kopf'.format(ctx.author))
        else:
            await ctx.send('{0.mention} Zahl'.format(ctx.author))

    @commands.command(aliases=['tableflip'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def flip(self, ctx):
        await ctx.send('{0.mention} (╯°□°）╯︵ ┻━┻'.format(ctx.author))

    @commands.command(aliases=['mayo'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def mayonaise(self, ctx):
        await ctx.send('{0.mention} https://www.youtube.com/watch?v=hVtSkF-hBXE'.format(ctx.author))

    @commands.command(aliases=['carlo'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
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
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def hoever(self, ctx):
        await ctx.send('{0.mention} https://soundcloud.com/cvrofficial/hoever/s-eXVFz'.format(ctx.author))

    @commands.command(hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def matheisttoll(self, ctx):
        await ctx.send('{0.mention} Mathe ist magic!'.format(ctx.author))

    @commands.command(hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def matheistmagic(self, ctx):
        await ctx.send('{0.mention} Und wie Sie sehen, es funktioniert auf magische Weise. Magic Mathe!'.format(ctx.author))

    @commands.command(hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def error(self, ctx):
        await ctx.send('{0.mention} Claßen: Error heißt ich weigere mich!'.format(ctx.author))

    @commands.command(hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def spam(self, ctx):
        await ctx.send('{0.mention} selber Spam!'.format(ctx.author))

    @commands.command(aliases=['arschwienflixbus'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def saft(self, ctx):
        await ctx.send('{0.mention} https://youtu.be/bx1vOD1jlN8?t=27'.format(ctx.guild.get_member(627153086753931305)))

    @commands.command(aliases=['dumm','dunning','kruger','schlau'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def wissen(self, ctx, member: typing.Optional[discord.Member]):
        if not member:
            member = ctx.author
        if member.id == 196245963260559360:
            return
        await ctx.send('{0.mention} Einmal bitte durchlesen:\nhttps://de.wikipedia.org/wiki/Dunning-Kruger-Effekt'.format(member))

    @commands.command(aliases=['fhfilm','film','werbung'],hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def imagefilm(self, ctx):
        await ctx.send('{0.mention} https://www.youtube.com/watch?v=dvqUcB_3JPg'.format(ctx.author))


def setup(bot):
    bot.add_cog(Fun(bot))
