import discord
import typing
import os

from discord.ext import commands
from db import db_session, db_engine, Session

from models.state import State
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

    @commands.command(aliases=['gruppenphase'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def groupphase(self, ctx, type:  typing.Optional[str]):
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

                # delete groupphase
                State.delete('groupphase_isStarted')
                State.delete('groupphase_reaction_message')
                Groupphaseuser.deleteall()

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

        elif type == 'info':
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
        else:
            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'Bitte übergebe `start`, `stop` oder `info` als erstes Argument.'
            )

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)

    @commands.Cog.listener()
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
                    Groupphaseuser.set(payload.user_id)
                else:
                    channel = self.bot.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    user = discord.Member
                    user.id = payload.user_id
                    await message.remove_reaction(payload.emoji, user)

    @commands.Cog.listener()
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
