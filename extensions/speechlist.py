import discord
import os
import typing
import random

from discord.ext import commands
from db import db_session, db_engine, Session

from extensions.util import create_embed, EmbedColour
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

    @commands.group(aliases=['redeliste','rl'], hidden=True)
    async def speechlist(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = await create_embed( 'Verwende einen der folgenden Befehle für eine bessere Übersicht.', EmbedColour.INFO )
            embed.add_field(
                name = "Befehle:", value = "!redeliste help\n!redeliste h\n!rl help\n!rl h", inline = False
            )
            await ctx.send(ctx.author.mention, embed=embed)     

    @speechlist.command(aliases=['h','hilfe'])
    async def help(self, ctx):
        embed = await create_embed( 'Bei diesem command handelt es sich um eine einfache Redeliste, damit sich nicht alle ständig unterbrechen.', EmbedColour.INFO )
        embed.add_field(
            name = "Syntax", value = "Folgende Befehle sind möglich:\n- !rl <_parameter_>", inline = False
        )
        embed.add_field(
            name = "Befehle", value = "- !rl h => Ruft diese Nachricht auf.\n\t- !rl a => Fügt dich zur Redeliste hinzu.\n\t- !rl r => Entfernt dich von der Redeliste.\n\t- !rl p => Gibt die aktuelle Redeliste erneut aus.",
            inline = False)
        embed.add_field(
            name = 'Tutorenbefehle',
            value = '- !rl e <_erwähnung_> => Entfernt die angegebene Person von der Redeliste.\nBsp. => !rl e @FachschaftsBot\n\t- !rl d => Löscht die gesamte Redeliste.\n\t- !rl f => Fügt dich mit einer Tutorenpriorität oben auf die Redeliste hinzu.\n\t- !rl n => Entfernt den obersten Eintrag auf der Redeliste.\n\t- !rl all <_voice_channel_> => Fügt alle Mitglieder eines angegebenen Sprackchannels in zufälliger Reihenfolge zur Redeliste hinzu.',
            inline = False
        )
        await ctx.send(ctx.author.mention, embed=embed)

    @speechlist.command(aliases=['a'])
    async def add(self, ctx):
        speechlist = Speechlistmodel.get(ctx.channel.id, ctx.author.id)
        embed = None
        mention = ctx.author.mention
        if speechlist:
            embed = await create_embed( 'Du stehst bereits auf der Redeliste!', EmbedColour.ERROR )
                
        else:
            name = ctx.author.display_name
            Speechlistmodel.set(ctx.channel.id, ctx.author.id, name, False)

            new_list = Speechlistmodel.all(ctx.channel.id)
            embed = await buildMessage(new_list)
            mention = ctx.channel.mention

        await ctx.send( mention, embed=embed )

    @speechlist.command(aliases=['r'])
    async def remove(self, ctx):
        speechlist = Speechlistmodel.get(ctx.channel.id, ctx.author.id)
        embed = None
        mention = ctx.author.mention
        if not speechlist:
            embed = await create_embed( 'Du bist nicht auf der Redeliste eingetragen!', EmbedColour.ERROR )

        elif not Speechlistmodel.all(ctx.channel.id):
            embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )


        else:
            Speechlistmodel.delete(ctx.channel.id, ctx.author.id)
            new_list = Speechlistmodel.all(ctx.channel.id)

            if not new_list:
                embed = await create_embed( 'Die Redeliste ist jetzt leer. Jeder sollte dran gewesen sein :)', EmbedColour.INFO )

            else:
                embed = await buildMessage(new_list)
                mention = ctx.channel.mention

        await ctx.send(mention, embed=embed)

    @speechlist.command(aliases=['p'])
    async def print(self, ctx):
        act_list = Speechlistmodel.all(ctx.channel.id)
        embed = None
        mention = ctx.author.mention
        if not act_list:
            embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )

        else:
            embed = await buildMessage(act_list)
            mention = ctx.channel.mention
            
        await ctx.send(mention, embed=embed)

    @speechlist.command(aliases=['d','löschen'])
    @commands.has_any_role( 'FSR', 'TUTOR', 'Tutor' )
    async def delete(self, ctx):
        act_list = Speechlistmodel.all(ctx.channel.id)
        embed = None
        mention = ctx.author.mention
        if not act_list:
            embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )

        else:
            Speechlistmodel.deleteAll(ctx.channel.id)
            embed = await create_embed( 'Die Redeliste ist jetzt leer. Durch einen Tutor gelöscht!', EmbedColour.INFO )
            mention = ctx.channel.mention

        await ctx.send(mention, embed=embed)

    @speechlist.command(aliases=['e','entferne'])
    @commands.has_any_role( 'FSR', 'TUTOR', 'Tutor' )
    async def erase(self, ctx, mem: typing.Optional[discord.Member]):
        act_list = Speechlistmodel.all(ctx.channel.id)
        if not act_list:
            embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )

            await ctx.send(ctx.author.mention, embed=embed)
        else:
            if mem:
                user = mem
                is_member_on_speechlist = Speechlistmodel.get(ctx.channel.id, user.id)

                embed = None
                mention = ctx.author.mention
                if is_member_on_speechlist:
                    Speechlistmodel.delete(ctx.channel.id, user.id)
                    inner_embed = await create_embed( f'{mem.display_name} wurde von der Liste gelöscht!', EmbedColour.INFO )

                    await ctx.send(mention, embed=inner_embed)

                    new_list = Speechlistmodel.all(ctx.channel.id)
                    mention = ctx.channel.mention

                    if new_list:
                        embed = await buildMessage(new_list)
                        embed.title = "Neue Redeliste:"

                    else:
                        embed = await create_embed( 'Die Redeliste ist jetzt leer. Jeder sollte dran gewesen sein :)', EmbedColour.INFO ) 
                        
                else:
                    embed = await create_embed( f'{mem.display_name} steht nicht auf der Redeliste!', EmbedColour.ERROR )

                await ctx.send( mention, embed=embed )

            else:
                embed = await create_embed( 'Du musst einen Namen angeben, der von der Liste gelöscht werden soll!',
                                            EmbedColour.ERROR )

                await ctx.send( ctx.author.mention, embed=embed )  

    @speechlist.command(aliases=['first','f'])
    @commands.has_any_role( 'FSR', 'TUTOR', 'Tutor' )
    async def prio(self, ctx):
        speechlist = Speechlistmodel.get(ctx.channel.id, ctx.author.id)
        embed = None
        mention = ctx.author.mention
        if speechlist:
            embed = await create_embed( 'Du stehst bereits auf der Redeliste!', EmbedColour.ERROR )
                
        else:
            name = ctx.author.display_name
                
            Speechlistmodel.set(ctx.channel.id, ctx.author.id, name, True)

            new_list = Speechlistmodel.all(ctx.channel.id)
            embed = await buildMessage(new_list)
            mention = ctx.channel.mention

        await ctx.send( mention, embed=embed )

    @speechlist.command(aliases=['n'])
    @commands.has_any_role( 'FSR', 'TUTOR', 'Tutor' )
    async def next(self, ctx):
        first_entry = Speechlistmodel.first(ctx.channel.id)

        embed = None
        mention = ctx.author.mention
        if first_entry:
            Speechlistmodel.delete(ctx.channel.id, first_entry.member_id)

            new_list = Speechlistmodel.all(ctx.channel.id)

            if new_list:
                embed = await buildMessage(new_list)
                embed.title = "Neue Redeliste:"
                mention = ctx.channel.mention

            else:
                embed = await create_embed( 'Die Redeliste ist jetzt leer. Jeder sollte dran gewesen sein :)',
                                            EmbedColour.INFO )
                mention = ctx.channel.mention

        else:
            embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )

        await ctx.send( mention, embed=embed )

    @speechlist.command(aliases=['alle','channel','addall'])
    @commands.has_any_role( 'FSR', 'TUTOR', 'Tutor' )
    async def all(self, ctx, channel: typing.Optional[discord.VoiceChannel]):
        mention = ctx.author.mention
        embed = None
        if ctx.guild.voice_channels.count(channel) > 0:
            Speechlistmodel.deleteAll(ctx.channel.id)

            member_list = channel.members
            random.shuffle( member_list )

            for m in member_list:
                Speechlistmodel.set(ctx.channel.id, m.id, m.display_name, False )
        
            embed = await create_embed( f'Alle Teilnehmer aus {channel.name} wurden zur Redeliste hinzugefügt!', EmbedColour.SUCCESS )
            await ctx.send( mention, embed=embed )

            new_list = Speechlistmodel.all(ctx.channel.id)
            mention = ctx.channel.mention

            if new_list:
                embed = await buildMessage(new_list)
                embed.title = "Neue Redeliste:"

        else:
            embed = await create_embed( 'Du musst einen gültigen Voice Channel angeben, von dem aus alle Teilnehmer hinzugefügt werden sollen.', EmbedColour.ERROR )
        
        await ctx.send( mention, embed=embed )

    @delete.error
    async def speechlist_error(self, ctx, err):
        if isinstance(err, commands.MissingAnyRole):
            embed = await create_embed( 'Du hst nicht die benötigten Rechte für diesen Befehl!\nVersuche es nächstes Jahr noch einmal, wenn deine vielversprechende Tutorenbewerbung angenommen worden ist :)',
                                            EmbedColour.ERROR )

            await ctx.send(ctx.author.mention, embed=embed)
        

async def buildMessage(queue: Speechlist):
    text = ''
    it = 0
    for item in queue:
        it += 1
        text = text + str(it) + ". " + item.member_name + '\n'

    msg = await create_embed( 'Redeliste:', EmbedColour.SUCCESS, description_text = text )

    return msg

def setup(bot):
    bot.add_cog(Speechlist(bot))