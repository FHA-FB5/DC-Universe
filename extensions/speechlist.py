import discord
import os
import typing


from discord.ext import commands
from db import db_session, db_engine, Session

from models.speechlist import Speechlistmodel


class Speechlist(commands.Cog, name='Speechlist'):
    def __init__(self, bot):
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance( self.bot_user_id, str ) :
            self.bot_user_id = int( self.bot_user_id )

        self.tutor_role_id = os.getenv(
            'GUILD_TUTOR_ROLE'
        )
        if isinstance( self.tutor_role_id, str ) :
            self.tutor_role_id = int( self.tutor_role_id )
            
        self.fsr_role_id = os.getenv(
            'GUILD_FSR_ROLE'
        )
        if isinstance( self.fsr_role_id, str ) :
            self.fsr_role_id = int( self.fsr_role_id )

    @commands.command(aliases=['redeliste','rl'], hidden=True)
    async def speechlist(self, ctx, active:  typing.Optional[str], mem: typing.Optional[str]):
        if active:
            active = active.lower()
        
        tutor = ctx.guild.get_role( self.tutor_role_id )
        fsr = ctx.guild.get_role( self.fsr_role_id )
        
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
            speechlist = Speechlistmodel.get(ctx.channel.id, ctx.author.id)
            if speechlist:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Du stehst bereits auf der Redeliste!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
                
            else:
                name = ctx.author.display_name
                Speechlistmodel.set(ctx.channel.id, ctx.author.id, name, False)

                new_list = Speechlistmodel.all(ctx.channel.id)
                msg = buildMessage(new_list)
                await ctx.send(ctx.channel.mention, embed=msg)
 
        elif active == 'remove' or active == 'r':
            speechlist = Speechlistmodel.get(ctx.channel.id, ctx.author.id)
            if not speechlist:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Du bist nicht auf der Redeliste eingetragen!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
            elif not Speechlistmodel.all(ctx.channel.id):
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Die Redeliste ist leer!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                Speechlistmodel.delete(ctx.channel.id, ctx.author.id)
                new_list = Speechlistmodel.all(ctx.channel.id)
                if not new_list:
                    embed = discord.Embed(
                        colour = discord.Colour.blue(),
                        title = 'Die Redeliste ist jetzt leer. Jeder sollte dran gewesen sein :)'
                    )
                    await ctx.send(ctx.author.mention, embed=embed)
                else:
                    msg = buildMessage(new_list)
                    await ctx.send(ctx.channel.mention, embed=msg)
        
        elif active == 'print' or active == 'p':
            act_list = Speechlistmodel.all(ctx.channel.id)
            if not act_list:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Die Redeliste ist leer!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                msg = buildMessage(act_list)
                await ctx.send(ctx.channel.mention, embed=msg)
        
        elif (active == 'delete' or active == 'd' or active == 'clear') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):
            act_list = Speechlistmodel.all(ctx.channel.id)
            if not act_list:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Die Redeliste ist leer!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                Speechlistmodel.deleteAll(ctx.channel.id)
                embed = discord.Embed(
                    colour = discord.Colour.blue(),
                    title = 'Die Redeliste ist jetzt leer. Durch einen Tutor gelöscht!'
                )
                await ctx.send(ctx.author.mention, embed=embed)

        elif (active == 'erase' or active == 'e') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):
            act_list = Speechlistmodel.all(ctx.channel.id)
            if not act_list:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Die Redeliste ist leer!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                if mem:
                    user = ''
                    members = self.bot.get_all_members()
                    for member in members:
                        if member.display_name == mem:
                            user = member
                            members.close()

                    if user != '':
                        is_member_on_speechlist = Speechlistmodel.get(ctx.channel.id, user.id)
                    else:
                        is_member_on_speechlist = False

                    if is_member_on_speechlist:
                        Speechlistmodel.delete(ctx.channel.id, user.id)
                        embed = discord.Embed(
                            colour = discord.Colour.blue(),
                            title = f'{mem} wurde von der Liste gelöscht!'
                        )
                        await ctx.send(ctx.author.mention, embed=embed)
                        new_list = Speechlistmodel.all(ctx.channel.id)
                        if new_list:
                            msg = buildMessage(new_list)
                            msg.title = "Neue Redeliste:"
                            await ctx.send(ctx.author.mention, embed=msg)
                        else:
                            embed = discord.Embed(
                            colour = discord.Colour.blue(),
                            title = 'Die Redeliste ist jetzt leer. Jeder sollte dran gewesen sein :)'
                            )
                            await ctx.send(ctx.author.mention, embed=embed) 

                    else:
                        embed = discord.Embed(
                            colour = discord.Colour.red(),
                            title = f'{mem} steht nicht auf der Redeliste!'
                        )
                        await ctx.send(ctx.author.mention, embed=embed)

                else:
                    embed = discord.Embed(
                        colour = discord.Colour.red(),
                        title = 'Du musst einen Namen angeben, der von der Liste gelöscht werden soll!'
                    )
                    await ctx.send(ctx.author.mention, embed=embed)

        elif (active == 'prio' or active == 'first') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):
            speechlist = Speechlistmodel.get(ctx.channel.id, ctx.author.id)
            if speechlist:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = 'Du stehst bereits auf der Redeliste!'
                )
                await ctx.send(ctx.author.mention, embed=embed)
                
            else:
                name = ctx.author.display_name
                
                Speechlistmodel.set(ctx.channel.id, ctx.author.id, name, True)

                new_list = Speechlistmodel.all(ctx.channel.id)
                msg = buildMessage(new_list)
                await ctx.send(ctx.channel.mention, embed=msg)
                
        # todo add all to list for tutors
        #elif (active == 'all' or active == 'a' or active == 'complete') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):
            
        else:
            embed = discord.Embed(
                colour = discord.Colour.blue(),
                title = 'Verwende einen der folgenden Befehle für eine bessere Übersicht.'
            )
            embed.add_field(
                name = "Befehle:", value = "!redeliste help\n!redeliste h\n!rl help\n!rl h", inline = False
            )
            await ctx.send(ctx.author.mention, embed=embed)

        

def buildMessage(queue: Speechlist):
    text = ''
    it = 0
    for item in queue:
        it += 1
        text = text + str(it) + ". " + item.member_name + '\n'

    msg = discord.Embed(
        colour = discord.Colour.green(),
        title = f'Redeliste:',
        description = text
    )

    return msg

def setup(bot):
    bot.add_cog(Speechlist(bot))