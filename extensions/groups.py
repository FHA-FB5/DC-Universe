import discord
import typing
import os
import math
import random

from discord.ext import commands
from db import db_session, db_engine, Session

from models.state import State
from models.group import Group
from models.groupphaseuser import Groupphaseuser


class Groups(commands.Cog, name='Groups'):
    def __init__(self, bot):
        self.bot = bot

        self.guild_announcements_channel_id = os.getenv(
            'GUILD_ANNOUNCEMENTS_CHANNEL')
        if isinstance(self.guild_announcements_channel_id, str):
            self.guild_announcements_channel_id = int(
                self.guild_announcements_channel_id)

        self.bot_user_id = os.getenv(
            'BOT_USER_ID')
        if isinstance(self.bot_user_id, str):
            self.bot_user_id = int(
                self.bot_user_id)

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

        self.guild_fsr_role_id = os.getenv(
            'GUILD_FSR_ROLE'
        )
        if isinstance(self.guild_fsr_role_id, str):
            self.guild_fsr_role_id = int(
                self.guild_fsr_role_id
            )

        self.guild_tutor_role_id = os.getenv(
            'GUILD_TUTOR_ROLE'
        )
        if isinstance(self.guild_tutor_role_id, str):
            self.guild_tutor_role_id = int(
                self.guild_tutor_role_id
            )

        self.guild_id = os.getenv(
            'GUILD_ID'
        )
        if isinstance(self.guild_id, str):
            self.guild_id = int(
                self.guild_id
            )

        self.guild = self.bot.get_guild(self.guild_id)
        self.guild_inf_role = self.guild.get_role(self.guild_inf_role_id)
        self.guild_wi_role = self.guild.get_role(self.guild_wi_role_id)
        self.guild_et_role = self.guild.get_role(self.guild_et_role_id)
        self.guild_mcd_role = self.guild.get_role(self.guild_mcd_role_id)
        self.guild_fsr_role = self.guild.get_role(self.guild_fsr_role_id)
        self.guild_tutor_role = self.guild.get_role(self.guild_tutor_role_id)

    @commands.command(aliases=['gruppenphase'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def groupphase(self, ctx, type:  typing.Optional[str], groupamount: typing.Optional[int]):
        if type:
            type = type.lower()

        if type == 'start':
            # check if grouphase is already startet
            state_groupphase_isStarted = State.get('groupphase_isStarted')
            if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es läuft schon eine Gruppenphase! Beende erst die alte, bevor du eine neue startest.'
                )

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

            else:

                # check if guild_announcements_channel_id isset
                if self.guild_announcements_channel_id > 0:
                    guild_announcements_channel = self.bot.get_channel(
                        self.guild_announcements_channel_id)

                    # check if channel was found
                    if guild_announcements_channel:
                        announcement_message = await guild_announcements_channel.send('Hallo @everyone,\neine neue Gruppenphase wurde gerade gestartet! Wenn du mitmachen willst, reagiere einfach mit einem :white_check_mark: auf diese Nachricht!')
                        await announcement_message.add_reaction('✅')

                        # start groupphase
                        State.set('groupphase_isStarted', str(True))
                        State.set('groupphase_reaction_message',
                                  announcement_message.id)

                        # create output embed
                        embed = discord.Embed(
                            colour=discord.Colour.green(),
                            title=f'Die Gruppenphase wurde erfolgreich gestartet!'
                        )

                        # send embed
                        await ctx.send(ctx.author.mention, embed=embed)

                    else:
                        # create output embed
                        embed = discord.Embed(
                            colour=discord.Colour.red(),
                            title=f'Der Ankündigung-Kanal wurde nicht gefunden. Überprüfe in der `.env`-Datei den Parameter `GUILD_ANNOUNCEMENTS_CHANNEL`.'
                        )

                        # send embed
                        await ctx.send(ctx.author.mention, embed=embed)

                else:
                    # create output embed
                    embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f'Bitte setze in der `.env`-Datei den Parameter `GUILD_ANNOUNCEMENTS_CHANNEL`.'
                    )

                    # send embed
                    await ctx.send(ctx.author.mention, embed=embed)

        elif type == 'stop':
            # check if grouphase is startet
            state_groupphase_isStarted = State.get('groupphase_isStarted')
            if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):

                # delete all groups
                for group in Group.all():
                    try:
                        await ctx.guild.get_role(group.role).delete()
                    except Exception:
                        pass

                    try:
                        await ctx.guild.get_channel(group.textChannel).delete()
                    except Exception:
                        pass

                    try:
                        await ctx.guild.get_channel(group.voiceChannel).delete()
                    except Exception:
                        pass

                    Group.delete(group.id)

                # delete groupphase user
                Groupphaseuser.deleteall()

                # delete groupphase
                State.delete('groupphase_isStarted')
                State.delete('groupphase_reaction_message')

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f'Die Gruppenphase wurde erfolgreich beendet!'
                )

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

            else:

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es läuft keine Gruppenphase, die du beenden könntest!'
                )

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

        elif type in ['shuffle']:
            # check if grouphase is startet
            state_groupphase_isStarted = State.get('groupphase_isStarted')
            if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):

                # check if groupamount parameter isset
                if groupamount:
                    if groupamount < 1:
                        groupamount = 1
                    elif groupamount > 20:
                        groupamount = 20

                    # create output embed
                    embed = discord.Embed(
                        colour=discord.Colour.blue(),
                        title="Neueinteilung der Gruppenphase beginnt",
                    )

                else:

                    # create output embed
                    embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f'Bitte füge noch den Parameter `groupamount` hinzu.'
                    )

                    # send embed
                    await ctx.send(ctx.author.mention, embed=embed)

        elif type in ['sort', 'inf', 'wi', 'et', 'mcd']:
            # check if grouphase is startet
            state_groupphase_isStarted = State.get('groupphase_isStarted')
            if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):

                # check if groupamount parameter isset
                if groupamount:
                    if groupamount < 2:
                        groupamount = 2
                    elif groupamount > 100:
                        groupamount = 100

                    # create output embed
                    embed = discord.Embed(
                        colour=discord.Colour.blue(),
                        title="Einteilung der Gruppenphase beginnt",
                    )

                    if type == 'sort':
                        members_total = len(Groupphaseuser.all())
                        embed.add_field(name='Teilnehmer',
                                        value=f'{members_total}', inline=False)
                    elif type == 'inf':
                        members_total = len(Groupphaseuser.inf())
                        embed.add_field(name='Teilnehmer (INF)',
                                        value=f'{members_total}', inline=False)
                    elif type == 'wi':
                        members_total = len(Groupphaseuser.wi())
                        embed.add_field(name='Teilnehmer (WI)',
                                        value=f'{members_total}', inline=False)
                    elif type == 'et':
                        members_total = len(Groupphaseuser.et())
                        embed.add_field(name='Teilnehmer (ET)',
                                        value=f'{members_total}', inline=False)
                    elif type == 'mcd':
                        members_total = len(Groupphaseuser.mcd())
                        embed.add_field(name='Teilnehmer (MCD)',
                                        value=f'{members_total}', inline=False)

                    embed.add_field(name='Gruppenanzahl',
                                    value=f'{groupamount}', inline=False)
                    embed.add_field(name='Max. Teilnehmer pro Gruppe',
                                    value=f'{math.ceil(members_total/groupamount)}', inline=False)

                    # send message
                    await ctx.send(ctx.author.mention, embed=embed)

                    for x in range(groupamount):
                        if type == 'sort':
                            groupname = 'Gruppe ' + str(x)
                        else:
                            groupname = type.upper() + '-Gruppe ' + str(x)

                        role = await ctx.guild.create_role(name=groupname, hoist=False)

                        overwrites = {
                            ctx.guild.default_role: discord.PermissionOverwrite(
                                view_channel=False,
                                read_messages=False,
                                connect=False,
                            ),
                            role: discord.PermissionOverwrite(
                                view_channel=True,
                                read_messages=True,
                                connect=True,
                            )
                        }
                        voiceChannel = await ctx.guild.create_voice_channel(name=groupname, overwrites=overwrites)
                        textChannel = await ctx.guild.create_text_channel(name=groupname, overwrites=overwrites)

                        group = Group(groupname, role.id,
                                      voiceChannel.id, textChannel.id)
                        if type == 'inf':
                            group.course = "inf"
                        elif type == 'wi':
                            group.course = "wi"
                        elif type == 'et':
                            group.course = "et"
                        elif type == 'mcd':
                            group.course = "mcd"

                        db_session.add(group)
                        db_session.commit()

                    # create output embed
                    embed = discord.Embed(
                        colour=discord.Colour.green(),
                        title=f'Gruppen erfolgreich angelegt!'
                    )

                    # send embed
                    await ctx.send(ctx.author.mention, embed=embed)

                    # create output embed
                    embed = discord.Embed(
                        colour=discord.Colour.blue(),
                        title=f'Beginne mit der Einteilung der Teilnehmer.'
                    )

                    # send embed
                    await ctx.send(ctx.author.mention, embed=embed)

                    if type == 'sort':
                        groups = Group.all()
                        allWithoutGroups = Groupphaseuser.allWithoutGroup()
                    elif type == 'inf':
                        groups = Group.inf()
                        allWithoutGroups = Groupphaseuser.allWithoutGroupInf()
                    elif type == 'wi':
                        groups = Group.wi()
                        allWithoutGroups = Groupphaseuser.allWithoutGroupWi()
                    elif type == 'et':
                        groups = Group.et()
                        allWithoutGroups = Groupphaseuser.allWithoutGroupEt()
                    elif type == 'mcd':
                        groups = Group.mcd()
                        allWithoutGroups = Groupphaseuser.allWithoutGroupMcd()
                    else:
                        return

                    counter = 0

                    for user in allWithoutGroups:
                        if counter >= groupamount:
                            counter = 0

                        user.groupID = groups[counter].id
                        userDiscord = ctx.guild.get_member(user.id)
                        role = ctx.guild.get_role(groups[counter].role)
                        await userDiscord.add_roles(role)

                        counter += 1
                        db_session.commit()

                    # create output embed
                    embed = discord.Embed(
                        colour=discord.Colour.green(),
                        title=f'Teilnehmer erfolgreich eingeteilt!'
                    )

                    # send embed
                    await ctx.send(ctx.author.mention, embed=embed)

                else:

                    # create output embed
                    embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f'Bitte füge noch den Parameter `groupamount` hinzu.'
                    )

                    # send embed
                    await ctx.send(ctx.author.mention, embed=embed)

            else:

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es läuft keine Gruppenphase, die du einteilen könntest!'
                )

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

        else:

            # check if grouphase is startet
            state_groupphase_isStarted = State.get('groupphase_isStarted')
            if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.blue(),
                    title="Informationen zur Gruppenphase",
                )

                members_total = len(Groupphaseuser.all())

                embed.add_field(name='Teilnehmer',
                                value=f'{members_total}', inline=False)

                inf_total = len(Groupphaseuser.inf())

                embed.add_field(name='INF',
                                value=f'{inf_total}', inline=False)

                wi_total = len(Groupphaseuser.wi())

                embed.add_field(name='WI',
                                value=f'{wi_total}', inline=False)

                et_total = len(Groupphaseuser.et())

                embed.add_field(name='ET',
                                value=f'{et_total}', inline=False)

                mcd_total = len(Groupphaseuser.mcd())

                embed.add_field(name='MCD',
                                value=f'{mcd_total}', inline=False)

                # send message
                await ctx.send(ctx.author.mention, embed=embed)

            else:

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title=f'Es läuft keine Gruppenphase, über die du Informationen anfodern kannst!'
                )

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['gruppe'])
    async def group(self, ctx):
        # check if grouphase is startet
        state_groupphase_isStarted = State.get('groupphase_isStarted')
        if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):

            # check channel
            current_group = Group.getByTextChannelId(ctx.channel.id)
            if current_group:

                # create output embed
                embed = discord.Embed(
                    colour=discord.Colour.blue(),
                    title=f'Gruppe: {current_group.name}'
                )

                # get members
                current_members = Groupphaseuser.getAllByGroupID(
                    current_group.id)
                current_members_total = len(current_members)

                embed.add_field(name='Teilnehmeranzahl',
                                value=f'{current_members_total}', inline=False)

                # get users
                current_user_list = []
                for member in current_members:
                    try:
                        current_user_list.append(self.bot.get_user(member.id))
                    except Exception:
                        pass

                if len(current_user_list) > 0:
                    output = ', '.join((u.mention for u in current_user_list))
                    embed.add_field(name='Teilnehmer',
                                    value=f'{output}', inline=False)

                # send embed
                await ctx.send(ctx.author.mention, embed=embed)

    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # check if bot react
        if payload.user_id == self.bot_user_id:
            return

        # check if grouphase is startet
        state_groupphase_isStarted = State.get('groupphase_isStarted')
        if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):
            state_groupphase_reaction_message = State.get(
                'groupphase_reaction_message')
            if (state_groupphase_reaction_message and int(state_groupphase_reaction_message.value) == payload.message_id):

                # check emoji
                if payload.emoji.name == '✅':

                    if (self.guild_fsr_role in payload.member.roles or self.guild_tutor_role in payload.member.roles):
                        channel = self.bot.get_channel(payload.channel_id)
                        message = await channel.fetch_message(payload.message_id)
                        user = discord.Member
                        user.id = payload.user_id
                        await message.remove_reaction(payload.emoji, user)
                    else:
                        course = 'no'

                        if self.guild_inf_role in payload.member.roles:
                            course = 'inf'
                        elif self.guild_wi_role in payload.member.roles:
                            course = 'wi'
                        elif self.guild_et_role in payload.member.roles:
                            course = 'et'
                        elif self.guild_mcd_role in payload.member.roles:
                            course = 'mcd'

                        if course != 'no':
                            Groupphaseuser.set(payload.user_id, course)
                        else:
                            channel = self.bot.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)
                            user = discord.Member
                            user.id = payload.user_id
                            await message.remove_reaction(payload.emoji, user)

                else:
                    channel = self.bot.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    user = discord.Member
                    user.id = payload.user_id
                    await message.remove_reaction(payload.emoji, user)

    @ commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # check if bot react
        if payload.user_id == self.bot_user_id:
            return

        # check if grouphase is startet
        state_groupphase_isStarted = State.get('groupphase_isStarted')
        if (state_groupphase_isStarted and state_groupphase_isStarted.value == str(True)):
            state_groupphase_reaction_message = State.get(
                'groupphase_reaction_message')
            if (state_groupphase_reaction_message and int(state_groupphase_reaction_message.value) == payload.message_id):

                # check emoji
                if payload.emoji.name == '✅':
                    Groupphaseuser.delete(payload.user_id)


def setup(bot):
    bot.add_cog(Groups(bot))
