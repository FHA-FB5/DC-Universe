import discord
import os
import typing
import urllib.request
import pytz

from datetime import datetime, tzinfo
from discord.ext import commands
from models.state import State


class ManualGroups(commands.Cog, name='ManualGroups'):
    def __init__(self, bot):
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance(self.bot_user_id, str):
            self.bot_user_id = int(self.bot_user_id)

        self.guild_id = os.getenv(
            'GUILD_ID'
        )
        if isinstance(self.guild_id, str):
            self.guild_id = int(
                self.guild_id
            )

        self.guild_study_course_channel_id = os.getenv(
            'GUILD_STUDY_COURSE_CHANNEL'
        )
        if isinstance(self.guild_study_course_channel_id, str):
            self.guild_study_course_channel_id = int(
                self.guild_study_course_channel_id
            )

        self.guild_announcement_channel_id = os.getenv(
            'GUILD_ANNOUNCEMENTS_CHANNEL'
        )
        if isinstance(self.guild_announcement_channel_id, str):
            self.guild_announcement_channel_id = int(
                self.guild_announcement_channel_id
            )

        self.guild_inf_role_id = os.getenv(
            'GUILD_INF_ROLE'
        )
        if isinstance(self.guild_inf_role_id, str):
            self.guild_inf_role_id = int(
                self.guild_inf_role_id
            )

        self.guild_wi_role_id = os.getenv(
            'GUILD_WI_ROLE'
        )
        if isinstance(self.guild_wi_role_id, str):
            self.guild_wi_role_id = int(
                self.guild_wi_role_id
            )

        self.guild_et_role_id = os.getenv(
            'GUILD_ET_ROLE'
        )
        if isinstance(self.guild_et_role_id, str):
            self.guild_et_role_id = int(
                self.guild_et_role_id
            )

        self.guild_mcd_role_id = os.getenv(
            'GUILD_MCD_ROLE'
        )
        if isinstance(self.guild_mcd_role_id, str):
            self.guild_mcd_role_id = int(
                self.guild_mcd_role_id
            )
        
        self.guild_tutor_role_id = os.getenv(
            'GUILD_TUTOR_ROLE'
        )
        if isinstance(self.guild_tutor_role_id, str):
            self.guild_tutor_role_id = int(
                self.guild_tutor_role_id
            )

        self.guild_fsr_role_id = os.getenv(
            'GUILD_FSR_ROLE'
        )
        if isinstance(self.guild_fsr_role_id, str):
            self.guild_fsr_role_id = int(
                self.guild_fsr_role_id
            )

    @commands.command(aliases=['studiengang', 'sg'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def studyProgram(self, ctx, active: typing.Optional[str]):
        if active:
            active = active.lower()

        # in general we does not care whether a message was already send or not

        # post message with content
        if active == 'start':
            guild_study_course_message = State.get(
                'guild_study_course_message')

            if guild_study_course_message:
                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es existiert bereits eine Nachricht, welche die Verteilung der Studiengänge behandelt.'
                )

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)
                return

            if self.guild_study_course_channel_id > 0:
                guild_study_course_channel = self.bot.get_channel(
                    self.guild_study_course_channel_id
                )

                if guild_study_course_channel:
                    command_message = await guild_study_course_channel.send(
                        'Hallo @everyone,\n' +
                        'Ab sofort könnt ihr euch eurem Studiengang zuordnen! Dies passiert indem du auf diese Nachricht reagierst.\n' +
                        'Die entsprechenden Buchstaben sind wie folgt zu verstehen:\n' +
                        ':regional_indicator_i: - Informatik\n' +
                        ':regional_indicator_w: - Wirtschaftsinformatik\n' +
                        ':regional_indicator_e: - Elektrotechnik\n' +
                        ':regional_indicator_m: - Media and Communications for Digital Business'
                    )
                    await command_message.add_reaction('🇮')
                    await command_message.add_reaction('🇼')
                    await command_message.add_reaction('🇪')
                    await command_message.add_reaction('🇲')
                    if command_message:
                        State.set('guild_study_course_message',
                                  command_message.id)

        if active == 'stopp':
            guild_study_course_message = State.get(
                'guild_study_course_message')

            if guild_study_course_message:
                channel = self.bot.get_channel(
                    self.guild_study_course_channel_id)
                msg = await channel.fetch_message(int(guild_study_course_message.value))
                if msg:
                    await msg.delete()
                State.delete('guild_study_course_message')
            else:
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es existiert keine Nachricht, welche die Verteilung der Studiengänge behandelt.'
                )
                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # check if bot react
        if payload.user_id == self.bot_user_id:
            return

        guild_study_course_message = State.get(
            'guild_study_course_message')

        if guild_study_course_message:

            channel = self.bot.get_channel(
                self.guild_study_course_channel_id
            )

            if (guild_study_course_message and int(guild_study_course_message.value) == payload.message_id):

                guild = self.bot.get_guild(payload.guild_id)

                msg = await channel.fetch_message(int(guild_study_course_message.value))

                role_inf = guild.get_role(self.guild_inf_role_id)
                role_wi = guild.get_role(self.guild_wi_role_id)
                role_mcd = guild.get_role(self.guild_mcd_role_id)
                role_et = guild.get_role(self.guild_et_role_id)

                if payload.emoji.name == '🇮':
                    await payload.member.add_roles(role_inf)
                    await payload.member.remove_roles(role_wi, role_mcd, role_et)

                elif payload.emoji.name == '🇼':
                    await payload.member.add_roles(role_wi)
                    await payload.member.remove_roles(role_inf, role_mcd, role_et)

                elif payload.emoji.name == '🇪':
                    await payload.member.add_roles(role_et)
                    await payload.member.remove_roles(role_wi, role_mcd, role_inf)

                elif payload.emoji.name == '🇲':
                    await payload.member.add_roles(role_mcd)
                    await payload.member.remove_roles(role_wi, role_inf, role_et)

                await msg.remove_reaction(payload.emoji, payload.member)

    @commands.command(aliases=['c', 'count', 'wieviele'], hidden=True)
    async def studyCourseCount(self, ctx, role: typing.Optional[str]):
        
        guild = ctx.guild
        all_member = self.bot.get_all_members()
        inf = guild.get_role( self.guild_inf_role_id )
        wi = guild.get_role( self.guild_wi_role_id )
        et = guild.get_role( self.guild_et_role_id )
        mcd = guild.get_role( self.guild_mcd_role_id )
        tutor = guild.get_role( self.guild_tutor_role_id )
        fsr = guild.get_role( self.guild_fsr_role_id )

        if role:
            role = role.lower()
            # remove whitespaces
            role = role.replace(' ', '')

            if role == 'inf' or role == 'informatik':
                inf_member = []
                for m in all_member:
                    if m.roles.count( inf ) >= 1:
                        inf_member.append( m )

                member_count = len(inf_member)
                online_count = 0
                for m in inf_member:
                    if m.status != discord.Status.offline:
                        online_count += 1

                fancy = ''
                von = ''
                if online_count != 0:
                    fancy = 'sind**'
                    von = ' von'
                else:
                    fancy = 'sind **keine'
                    online_count = ''
                    member_count = ''

                embed = discord.Embed(
                    colour = inf.colour,
                    title = 'Informatiker auf dem Server:',
                    description = f'Es {fancy} {online_count}{von} {member_count} Studierenden** online.'
                )

            elif role == 'wi' or role == 'wirtschaft' or role == 'wirtschaftsinformatik':
                wi_member = []
                for m in all_member:
                    if m.roles.count( wi ) >= 1:
                        wi_member.append( m )

                member_count = len(wi_member)
                online_count = 0
                for m in wi_member:
                    if m.status != discord.Status.offline:
                        online_count += 1


                fancy = ''
                von = ''
                if online_count != 0:
                    fancy = 'sind**'
                    von = ' von'
                else:
                    fancy = 'sind **keine'
                    online_count = ''
                    member_count = ''

                embed = discord.Embed(
                    colour = wi.colour,
                    title = 'Wirtschaftsinformatiker auf dem Server:',
                    description = f'Es {fancy} {online_count}{von} {member_count} Studierenden** online.'
                )
      
            elif role == 'et' or role == 'etec' or role == 'etechnik' or role == 'elektrotechnik':
                et_member = []
                for m in all_member:
                    if m.roles.count( et ) >= 1:
                        et_member.append( m )

                member_count = len(et_member)
                online_count = 0
                for m in et_member:
                    if m.status != discord.Status.offline:
                        online_count += 1

                fancy = ''
                von = ''
                if online_count != 0:
                    fancy = 'sind**'
                    von = ' von'
                else:
                    fancy = 'sind **keine'
                    online_count = ''
                    member_count = ''

                embed = discord.Embed(
                    colour = et.colour,
                    title = 'Elektrotechniker auf dem Server:',
                    description = f'Es {fancy} {online_count}{von} {member_count} Studierenden** online.'
                )

            elif role == 'mcd' or role == 'media' or role == 'mediaandcommunication' or role == 'irgendwasmitmedien':
                mcd_member = []
                for m in all_member:
                    if m.roles.count( mcd ) >= 1:
                        mcd_member.append( m )

                member_count = len(mcd_member)
                online_count = 0
                for m in mcd_member:
                    if m.status != discord.Status.offline:
                        online_count += 1

                fancy = ''
                von = ''
                if online_count != 0:
                    fancy = 'sind**'
                    von = ' von'
                else:
                    fancy = 'sind **keine'
                    online_count = ''
                    member_count = ''

                embed = discord.Embed(
                    colour = mcd.colour,
                    title = 'MCDler auf dem Server (sry Name ist zu lang):',
                    description = f'Es {fancy} {online_count}{von} {member_count} Studierenden** online.'
                )

            elif role == 'tut' or role == 'tutor' or role == 'esa':
                tut_member = []
                for m in all_member:
                    if m.roles.count( tutor ) >= 1:
                        tut_member.append( m ) 

                member_count = len(tut_member)
                online_count = 0
                for m in tut_member:
                    if m.status != discord.Status.offline:
                        online_count += 1

                fancy = ''
                von = ''
                if online_count != 0:
                    fancy = 'sind**'
                    von = ' von'
                else:
                    fancy = 'sind **keine'
                    online_count = ''
                    member_count = ''

                embed = discord.Embed(
                    colour = tutor.colour,
                    title = 'Tutoren auf dem Server:',
                    description = f'Es {fancy} {online_count}{von} {member_count} Studierenden** online.'
                )
            
            elif role == 'fsr' or role == 'fachschaft' or role == 'rat':
                fsr_member = []
                for m in all_member:
                    if m.roles.count( fsr ) >= 1:
                        fsr_member.append( m ) 

                member_count = len(fsr_member)
                online_count = 0
                for m in fsr_member:
                    if m.status != discord.Status.offline:
                        online_count += 1

                fancy = ''
                von = ''
                if online_count != 0:
                    fancy = 'sind**'
                    von = ' von'
                else:
                    fancy = 'sind **keine'
                    online_count = ''
                    member_count = ''

                embed = discord.Embed(
                    colour = fsr.colour,
                    title = 'FSRler auf dem Server:',
                    description = f'Es {fancy} {online_count}{von} {member_count} Studierenden** online.'
                )
            
            await ctx.send( ctx.author.mention, embed=embed )
        
        else:
            
            date = datetime.now(pytz.timezone('Etc/GMT+1'))
            embed = discord.Embed(
                colour = 0x00b5ad,
                title = 'Die Verteilung von Mitgliedern auf dem Server',
                description = 'Eine aktuelle Auflistung',
                timestamp = date               
            )
            embed.set_footer( text = 'Statistiken', icon_url='https://i.imgur.com/WBeaODR.jpg' )

            member = [[], [], [], [], [], []]
            all_count = 0
            all_online = 0

            for m in all_member:
                all_count += 1
                if m.status != discord.Status.offline:
                    all_online += 1
                if m.roles.count( inf ) >= 1:
                    member[0].append( m )
                elif m.roles.count( wi ) >= 1:
                    member[1].append( m )
                elif m.roles.count( et ) >= 1:
                    member[2].append( m )
                elif m.roles.count( mcd ) >= 1:
                    member[3].append( m )
                elif m.roles.count( tutor ) >= 1:
                    member[4].append( m )
                elif m.roles.count( fsr ) >= 1:
                    member[5].append( m )
            
            inf_count = len(member[0])
            wi_count = len(member[1])
            et_count = len(member[2])
            mcd_count = len(member[3])
            tut_count = len(member[4])
            fsr_count = len(member[5])
            online = 0
        
            # inf field
            for m in member[0]:
                if m.status != discord.Status.offline:
                    online += 1
            
            fancy = ''
            von = ''
            if online != 0:
                fancy = 'sind**'
                von = ' von'
            else:
                fancy = 'sind **keine'
                online = ''
                inf_count = ''

            embed.add_field(
                name = 'Informatiker auf dem Server:',
                value = f'Es {fancy} {online}{von} {inf_count} Studierenden** online.',
                inline = False
            )

            # wi field
            online = 0
            for m in member[1]:
                if m.status != discord.Status.offline:
                    online += 1
            
            fancy = ''
            von = ''
            if online != 0:
                fancy = 'sind**'
                von = ' von'
            else:
                fancy = 'sind **keine'
                online = ''
                wi_count = ''

            embed.add_field(
                name = 'Wirtschaftsinformatiker auf dem Server:',
                value = f'Es {fancy} {online}{von} {wi_count} Studierenden** online.',
                inline = False
            )

            # et field
            online = 0
            for m in member[2]:
                if m.status != discord.Status.offline:
                    online += 1
            
            fancy = ''
            von = ''
            if online != 0:
                fancy = 'sind**'
                von = ' von'
            else:
                fancy = 'sind **keine'
                online = ''
                et_count = ''

            embed.add_field(
                name = 'Elektrotechniker auf dem Server:',
                value = f'Es {fancy} {online}{von} {et_count} Studierenden** online.',
                inline = False
            )

            # mcd field
            online = 0
            for m in member[3]:
                if m.status != discord.Status.offline:
                    online += 1
            
            fancy = ''
            von = ''
            if online != 0:
                fancy = 'sind**'
                von = ' von'
            else:
                fancy = 'sind **keine'
                online = ''
                mcd_count = ''

            embed.add_field(
                name = 'MCDler auf dem Server:',
                value = f'Es {fancy} {online}{von} {mcd_count} Studierenden** online.',
                inline = False
            )

            # tutor field
            online = 0
            for m in member[4]:
                if m.status != discord.Status.offline:
                    online += 1
            
            fancy = ''
            von = ''
            if online != 0:
                fancy = 'sind**'
                von = ' von'
            else:
                fancy = 'sind **keine'
                online = ''
                tut_count = ''

            embed.add_field(
                name = 'Tutoren auf dem Server:',
                value = f'Es {fancy} {online}{von} {tut_count} Studierenden** online.',
                inline = False
            )

            # fsr field
            online = 0
            for m in member[5]:
                if m.status != discord.Status.offline:
                    online += 1
            
            fancy = ''
            von = ''
            if online != 0:
                fancy = 'sind**'
                von = ' von'
            else:
                fancy = 'sind **keine'
                online = ''
                fsr_count = ''

            embed.add_field(
                name = 'FSRler auf dem Server:',
                value = f'Es {fancy} {online}{von} {fsr_count} Studierenden** online.',
                inline = False
            )

            # all field
            fancy = ''
            von = ''
            if all_online != 0:
                fancy = 'sind**'
                von = ' von'
            else:
                fancy = 'sind **keine'
                online = ''
                all_count = ''

            embed.add_field(
                name = 'Insgesamt:',
                value = f'Es {fancy} {all_online}{von} {all_count} Studierenden** online.',
                inline = False
            )
            
            await ctx.send( ctx.author.mention, embed=embed )
        


def setup(bot):
    bot.add_cog(ManualGroups(bot))
