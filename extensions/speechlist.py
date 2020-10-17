import discord
import os
import typing


from discord.ext import commands


class Speechlist(commands.Cog, name='Speechlist'):
    def __init__(self, bot):
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance( self.bot_user_id, str ) :
            self.bot_user_id = int( self.bot_user_id )

        self.speech_list = []
        self.count = 0



    @commands.command(aliases=['redeliste','rl'], hidden=True)
    async def speechlist(self, ctx, active:  typing.Optional[str]):
        if active:
            active = active.lower()
        
        if active == 'help' or active == 'h':
            embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = f'Bei diesem command handelt es sich um eine einfache Redeliste, damit sich nicht alle ständig unterbrechen.'
            )
            embed.add_field(
                name = "Syntax", value = "Folgende Befehle sind möglich:\n- !rl|redeliste <parameter>", inline = False
            )
            embed.add_field(
                name = "Parameter", value = "- [h|help] Ruft diese Nachricht auf.\n\t- [a|add] Fügt dich zur Redeliste hinzu.\n\t- [r|remove] Entfernt dich von der Redeliste.\n\t- [p|print] Gibt die aktuelle Redeliste erneut aus.",
                inline = False)
            await ctx.send(ctx.author.mention, embed=embed)
        
        elif active == 'add' or active == 'a':
            if self.speech_list.count(ctx.author.nick) > 0:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Du stehst bereits auf der Redeliste!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
                
            else:
                self.speech_list.append(ctx.author.nick)
                self.count = self.count + 1
            
                msg = buildMessage(self.speech_list, self.count)
                await ctx.send(ctx.channel.mention, embed=msg)
 
        elif active == 'remove' or active == 'r':
            if self.speech_list.count(ctx.author.nick) == 0:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Du bist nicht auf der Redeliste eingetragen!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
            elif self.count == 0:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Die Redeliste ist leer!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                self.speech_list.remove(ctx.author.nick)
                self.count = self.count - 1

                if self.count == 0:
                    embed = discord.Embed(
                        colour = discord.Colour.blue(),
                        title = 'Die Redeliste ist jetzt leer. Jeder sollte dran gewesen sein :)'
                    )
                    await ctx.send(ctx.author.mention, embed=embed)
                else:
                    msg = buildMessage(self.speech_list, self.count)
                    await ctx.send(ctx.channel.mention, embed=msg)
        
        elif active == 'print' or active == 'p':
            if self.count == 0:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Die Redeliste ist leer!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                msg = buildMessage(self.speech_list, self.count)
                await ctx.send(ctx.channel.mention, embed=msg)

        else:
            embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = 'Verwende einen der folgenden Befehle für eine bessere Übersicht.'
            )
            embed.add_field(
                name = "Befehle:", value = "!redeliste help\n!redeliste h\n!rl help\n!rl h", inline = False
            )
            await ctx.send(ctx.author.mention, embed=embed)

def buildMessage(queue: list, count: int):
    tmp = queue.copy()
    text = ""
    it = 0
    while it < count:
        name = tmp.pop()
        it = it + 1
        text = text + str(it) + ". " + name + "\n"

    msg = discord.Embed(
        colour = discord.Colour.green(),
        title = f'Redeliste:',
        description = text
    )

    return msg

def setup(bot):
    bot.add_cog(Speechlist(bot))