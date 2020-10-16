import discord
import os
import typing
import urllib.request

from discord.ext import commands


class ManualGroups( commands.Cog, name='ManualGroups' ):
    def __init__(self, bot): 
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance( self.bot_user_id, str ) :
            self.bot_user_id = int( self.bot_user_id )

        self.guild_study_course_channel_id = os.getenv(
            'GUILD_STUDY_COURSE_CHANNEL' 
        )
        if isinstance( self.guild_study_course_channel_id, str ) :
            self.guild_study_course_channel_id = int(
                self.guild_study_course_channel_id 
            )
        
        self.guild_announcement_channel_id = os.getenv(
            'GUILD_ANNOUNCEMENTS_CHANNEL'
        )
        if isinstance( self.guild_announcement_channel_id, str ) :
            self.guild_announcement_channel_id = int(
                self.guild_announcement_channel_id
            )

        self.guild_inf_role_id = os.getenv(
            'GUILD_INF_ROLE' 
        )
        if isinstance( self.guild_inf_role_id, str ) :
            self.guild_inf_role_id = int(
                self.guild_inf_role_id 
            )

        self.guild_wi_role_id = os.getenv(
            'GUILD_WI_ROLE' 
        )
        if isinstance( self.guild_wi_role_id, str ) :
            self.guild_wi_role_id = int(
                self.guild_wi_role_id 
            )

        self.guild_et_role_id = os.getenv(
            'GUILD_ET_ROLE' 
        )
        if isinstance( self.guild_et_role_id, str ) :
            self.guild_et_role_id = int(
                self.guild_et_role_id 
            )

        self.guild_mcd_role_id = os.getenv(
            'GUILD_MCD_ROLE' 
        )
        if isinstance( self.guild_mcd_role_id, str ) :
            self.guild_mcd_role_id = int(
                self.guild_mcd_role_id
            )
        
        self.guild_command_message_id = 0
        self.guild_announcement_message_id = 0


    @commands.command(aliases=['studiengang', 'sg'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def studyProgram(self, ctx, active: typing.Optional[str]):
        if active:
            active = active.lower()

        # in general we does not care whether a message was already send or not

        # post message with content
        if active == 'start':
            if self.guild_command_message_id > 0:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es existiert bereits eine Nachricht, welche die Verteilung der Studiengänge behandelt.'
                )
                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
                return

            if self.guild_study_course_channel_id > 0:
                # guild_announcement_channel = self.bot.get_channel(
                #    self.guild_announcement_channel_id
                #)
                guild_study_course_channel = self.bot.get_channel(
                    self.guild_study_course_channel_id
                )

                if guild_study_course_channel :
                    command_message = await guild_study_course_channel.send(
                        'Hallo @everyone,\n' + 
                        'Ab sofort könnt ihr euch eurem Studiengang zuordnen! Dies passiert indem du auf diese Nachricht reagierst.\n' +
                        'Die entsprechenden Buchstaben sind wie folgt zu verstehen:\n' +
                        ':regional_indicator_i: - INF\n' +
                        ':regional_indicator_w: - WI\n' +
                        ':regional_indicator_e: - ET\n' +
                        ':regional_indicator_m: - MCD' 
                    )
                    await command_message.add_reaction('🇮')
                    await command_message.add_reaction('🇼')
                    await command_message.add_reaction('🇪')
                    await command_message.add_reaction('🇲')
                    if command_message:
                        await command_message.pin()
                        self.guild_command_message_id = command_message.id
                    
                    # embed = discord.Embed(
                    #    colour = discord.Colour.blue(),
                    #    title = f'Info:\nIm Channel <#{self.guild_study_course_channel_id}> könnt ihr euch einem Studiengang zuordnen'
                    #)
                    # announcement_message = await guild_announcement_channel.send(embed=embed)
                    #if announcement_message:
                    #    self.guild_announcement_message_id = announcement_message.id

        if active == 'stopp':
            if self.guild_command_message_id == 0:
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = f'Es existiert keine Nachricht, welche die Verteilung der Studiengänge behandelt.'
                )
                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
            
            else :
                channel = self.bot.get_channel( self.guild_study_course_channel_id )
                msg = await channel.fetch_message( self.guild_command_message_id )
                if msg:
                    await msg.unpin()
                    await msg.delete()
                channel = self.bot.get_channel( self.guild_announcement_channel_id )
                msg = await channel.fetch_message( self.guild_announcement_message_id )
                if msg:
                    await msg.unpin()
                    await msg.delete()
                self.guild_command_message_id = 0
                self.guild_announcement_message_id = 0


    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # check if bot react
        if payload.user_id == self.bot_user_id:
            return
        
        channel = self.bot.get_channel(
            self.guild_study_course_channel_id
        )

        if self.guild_command_message_id > 0 and self.guild_command_message_id == payload.message_id:

            guild = self.bot.get_guild(payload.guild_id)

            msg = await channel.fetch_message( self.guild_command_message_id )

            role_inf = guild.get_role(self.guild_inf_role_id)
            role_wi = guild.get_role(self.guild_wi_role_id)
            role_mcd = guild.get_role(self.guild_mcd_role_id)
            role_et = guild.get_role(self.guild_et_role_id)

            if payload.emoji.name == '🇮':
                await msg.remove_reaction('🇼', payload.member)
                await msg.remove_reaction('🇪', payload.member)
                await msg.remove_reaction('🇲', payload.member)
                await payload.member.remove_roles(role_wi, role_mcd, role_et)
                await payload.member.add_roles(role_inf)

            elif payload.emoji.name == '🇼':
                await msg.remove_reaction('🇮', payload.member)
                await msg.remove_reaction('🇪', payload.member)
                await msg.remove_reaction('🇲', payload.member)
                await payload.member.remove_roles(role_inf, role_mcd, role_et)
                await payload.member.add_roles(role_wi)

            elif payload.emoji.name == '🇪':
                await msg.remove_reaction('🇼', payload.member)
                await msg.remove_reaction('🇮', payload.member)
                await msg.remove_reaction('🇲', payload.member)
                await payload.member.remove_roles(role_wi, role_mcd, role_inf)
                await payload.member.add_roles(role_et)

            elif payload.emoji.name == '🇲':
                await msg.remove_reaction('🇼', payload.member)
                await msg.remove_reaction('🇪', payload.member)
                await msg.remove_reaction('🇮', payload.member)
                await payload.member.remove_roles(role_wi, role_inf, role_et)
                await payload.member.add_roles(role_mcd)
            else:
                message = await channel.fetch_message(payload.message_id)
                user = discord.Member
                user.id = payload.user_id
                await message.remove_reaction(payload.emoji, user)
                return

    @ commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # check if bot react
        if payload.user_id == self.bot_user_id:
            return
        
        if self.guild_command_message_id > 0 and self.guild_command_message_id == payload.message_id:

            user_id = payload.user_id
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(user_id)

            role_inf = guild.get_role(self.guild_inf_role_id)
            role_wi = guild.get_role(self.guild_wi_role_id)
            role_mcd = guild.get_role(self.guild_mcd_role_id)
            role_et = guild.get_role(self.guild_et_role_id)   

            if payload.emoji.name == '🇮':
                await member.remove_roles(role_inf)

            elif payload.emoji.name == '🇼':
                await member.remove_roles(role_wi)

            elif payload.emoji.name == '🇪':
                await member.remove_roles(role_et)    

            elif payload.emoji.name == '🇲':
                await member.remove_roles(role_mcd)

def setup( bot ):
    bot.add_cog( ManualGroups( bot ) )
