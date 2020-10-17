import discord
import os
import typing
import queue

from discord.ext import commands


class Speechlist(commands.Cog, name='Speechlist'):
    def __init__(self, bot):
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance( self.bot_user_id, str ) :
            self.bot_user_id = int( self.bot_user_id )

        self.msg = 0

        self.speech_queue = queue.PriorityQueue()

    async def on_message(self, message):
        if message.author.id == self.bot_user_id:
            return

        if message.content:
            message.content = message.content.lower()
            self.msg = message.content.split(" ")
        
        if self.msg[1] == 'help' or self.msg[1] == 'h':
            embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = f'Bei diesem command handelt es sich um eine einfache Redeliste, damit sich nicht alle ständig unterbrechen.'
            )
            embed.add_field(
                name = "Syntax", value = "Folgende Befehle sind möglich:\n- !rl|redeliste <parameter>", inline = False
            )
            embed.add_field(
                name = "Parameter", value = "- [h|help] Ruft diese Nachricht auf.\n\t- [a|add] Fügt dich zur Redeliste hinzu.\n\t- [r|remove] Entfernt dich von der Redeliste.\n\t",
                inline = False)
            await ctx.send(ctx.author.mention, embed=embed)
        
        elif self.msg[1] == 'add' or self.msg[1] == 'a':
            self.speech_queue.put(ctx.author)
            await ctx.send(self.speech_queue.get)

        elif self.msg[1] == 'remove' or self.msg[1] == 'r':
            return

        else:
            embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = 'Verwende einen der folgenden Befehle für eine bessere Übersicht.'
            )
            embed.add_field(
                name = "Befehle:", value = "!redeliste help\n!redeliste h\n!rl help\n!rl h", inline = False
            )
            await ctx.send(ctx.author.mention, embed=embed)



#    @commands.command(aliases=['redeliste','rl'], hidden=True)
#    async def speechlist(self, ctx, active:  typing.Optional[str]):
#        if active:
#            active = active.lower()
#        
#        if active == 'help' or active == 'h':
#            embed = discord.Embed(
#                colour = discord.Colour.blue(),
#                title = f'Bei diesem command handelt es sich um eine einfache Redeliste, damit sich nicht alle ständig unterbrechen.'
#            )
#            embed.add_field(
#                name = "Syntax", value = "Folgende Befehle sind möglich:\n- !rl|redeliste <parameter>", inline = False
#            )
#            embed.add_field(
#                name = "Parameter", value = "- [h|help] Ruft diese Nachricht auf.\n\t- [a|add] Fügt dich zur Redeliste hinzu.\n\t- [r|remove] Entfernt dich von der Redeliste.\n\t",
#                inline = False)
#            await ctx.send(ctx.author.mention, embed=embed)
#        
#        elif active == 'add' or active == 'a':
#            self.speech_queue.put(ctx.author)
#            await ctx.send(self.speech_queue.get)
#
#        elif active == 'remove' or active == 'r':
#            return
#
#        else:
#            embed = discord.Embed(
#                colour = discord.Colour.blue(),
#                title = 'Verwende einen der folgenden Befehle für eine bessere Übersicht.'
#            )
#            embed.add_field(
#                name = "Befehle:", value = "!redeliste help\n!redeliste h\n!rl help\n!rl h", inline = False
#            )
#            await ctx.send(ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Speechlist(bot))