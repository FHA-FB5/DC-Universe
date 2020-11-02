import discord
import os
import typing


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

    @commands.command(aliases=['redeliste','rl'], hidden=True)
    async def speechlist(self, ctx, active:  typing.Optional[str], mem: typing.Optional[discord.Member]):
        if active:
            active = active.lower()
        
        tutor = ctx.guild.get_role( self.tutor_role_id )
        fsr = ctx.guild.get_role( self.fsr_role_id )
        
        if active == 'help' or active == 'h':
            embed = await create_embed( 'Bei diesem command handelt es sich um eine einfache Redeliste, damit sich nicht alle ständig unterbrechen.', EmbedColour.INFO )
            embed.add_field(
                name = "Syntax", value = "Folgende Befehle sind möglich:\n- !rl <_parameter_>", inline = False
            )
            embed.add_field(
                name = "Befehle", value = "- !rl h => Ruft diese Nachricht auf.\n\t- !rl a => Fügt dich zur Redeliste hinzu.\n\t- !rl r => Entfernt dich von der Redeliste.\n\t- !rl p => Gibt die aktuelle Redeliste erneut aus.",
                inline = False)
            embed.add_field(
                name = 'Tutorenbefehle',
                value = '- !rl e <_erwähnung_> => Entfernt die angegebene Person von der Redeliste.\nBsp. => !rl e @FachschaftsBot\n\t- !rl d => Löscht die gesamte Redeliste.\n\t- !rl f => Fügt dich mit einer Tutorenpriorität oben auf die Redeliste hinzu.\n\t- !rl n => Entfernt den obersten Eintrag auf der Redeliste.',
                inline = False
            )
            await ctx.send(ctx.author.mention, embed=embed)
        
        elif active == 'add' or active == 'a':
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
 
        elif active == 'remove' or active == 'r':
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
        
        elif active == 'print' or active == 'p':
            act_list = Speechlistmodel.all(ctx.channel.id)
            embed = None
            mention = ctx.author.mention
            if not act_list:
                embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )

            else:
                embed = await buildMessage(act_list)
                mention = ctx.channel.mention
            
            await ctx.send(mention, embed=embed)
        
        elif (active == 'delete' or active == 'd' or active == 'clear') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):
            act_list = Speechlistmodel.all(ctx.channel.id)
            if not act_list:
                embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )

                await ctx.send(ctx.author.mention, embed=embed)
            else:
                Speechlistmodel.deleteAll(ctx.channel.id)
                embed = await create_embed( 'Die Redeliste ist jetzt leer. Durch einen Tutor gelöscht!', EmbedColour.INFO )

                await ctx.send(ctx.author.mention, embed=embed)

        elif (active == 'erase' or active == 'e') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):
            act_list = Speechlistmodel.all(ctx.channel.id)
            if not act_list:
                embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )

                await ctx.send(ctx.author.mention, embed=embed)
            else:
                if mem:
                    user = mem
                    is_member_on_speechlist = Speechlistmodel.get(ctx.channel.id, user.id)

                    if is_member_on_speechlist:
                        Speechlistmodel.delete(ctx.channel.id, user.id)
                        embed = await create_embed( f'{mem.display_name} wurde von der Liste gelöscht!', EmbedColour.INFO )

                        await ctx.send(ctx.author.mention, embed=embed)

                        new_list = Speechlistmodel.all(ctx.channel.id)
                        embed = None
                        mention = ctx.author.mention
                        if new_list:
                            embed = await buildMessage(new_list)
                            embed.title = "Neue Redeliste:"
                            mention = ctx.channel.mention
                        else:
                            embed = await create_embed( 'Die Redeliste ist jetzt leer. Jeder sollte dran gewesen sein :)', EmbedColour.INFO ) 
                        
                        await ctx.send(mention, embed=embed)

                    else:
                        embed = await create_embed( f'{mem.display_name} steht nicht auf der Redeliste!', EmbedColour.ERROR )

                        await ctx.send(ctx.author.mention, embed=embed)

                else:
                    embed = await create_embed( 'Du musst einen Namen angeben, der von der Liste gelöscht werden soll!',
                                                EmbedColour.ERROR )

                    await ctx.send(ctx.author.mention, embed=embed)

        elif (active == 'prio' or active == 'first' or active == 'f') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):
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

        elif (active == 'n' or active == 'next') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):
            first_entry = Speechlistmodel.first(ctx.channel.id)

            if first_entry:
                Speechlistmodel.delete(ctx.channel.id, first_entry.member_id)

                new_list = Speechlistmodel.all(ctx.channel.id)
                embed = None
                mention = ctx.author.mention
                if new_list:
                    embed = await buildMessage(new_list)
                    embed.title = "Neue Redeliste:"
                    mention = ctx.channel.mention

                else:
                    embed = await create_embed( 'Die Redeliste ist jetzt leer. Jeder sollte dran gewesen sein :)',
                                                EmbedColour.INFO )

                await ctx.send( mention, embed=embed )
            else:
                embed = await create_embed( 'Die Redeliste ist leer!', EmbedColour.ERROR )

                await ctx.send(ctx.author.mention, embed=embed)
                
        # todo add all to list for tutors
        #elif (active == 'all' or active == 'a' or active == 'complete') and (ctx.author.roles.count( tutor ) >= 1 or ctx.author.roles.count( fsr ) >= 1):

        elif (active == 'prio' or active == 'first' or active == 'delete' or active == 'd' or active == 'clear' or active == 'erase' or active == 'e' or active == 'n' or active == 'next'):
            embed = await create_embed( 'Du hst nicht die benötigten Rechte für diesen Befehl!\nVersuche es nächstes Jahr noch einmal, wenn deine vielversprechende Tutorenbewerbung angenommen worden ist :)',
                                        EmbedColour.ERROR )

            await ctx.send(ctx.author.mention, embed=embed)

        else:
            embed = await create_embed( 'Verwende einen der folgenden Befehle für eine bessere Übersicht.', EmbedColour.INFO )
            embed.add_field(
                name = "Befehle:", value = "!redeliste help\n!redeliste h\n!rl help\n!rl h", inline = False
            )
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