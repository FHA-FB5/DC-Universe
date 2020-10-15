import discord
import os
import typing

from discord.ext import commands


class ManualGroups( commands.Cog, name='ManualGroups' ):
    def __init__(self, bot): 
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance( self.bot_user_id, str ) :
            self.bot_user_id = int( self.bot_user_id )

        self.guild_command_channel_id = os.getenv(
            'GUILD_COMMAND_CHANNEL' 
        )
        if isinstance( self.guild_command_channel_id, str ) :
            self.guild_command_channel_id = int(
                self.guild_command_channel_id 
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


    @commands.command(aliases=['studiengang', 'sg'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def studyProgram(self, ctx, active: typing.Optional[str]):
        if active:
            active = active.lower()

        # in general we does not care whether a message was already send or not

        # post message with content
        if active == 'start':

            if self.guild_announcement_channel_id > 0 :
                guild_announcement_channel = self.bot.get_channel(
                    self.guild_announcement_channel_id
                )

                if guild_announcement_channel :
                    announcement_message = await guild_announcement_channel.send(
                        'Hallo @everyone,\n' + 
                        'Ab sofort könnt ihr euch eurem Studiengang zuordnen! Dies passiert indem du auf diese Nachricht reagierst.\n' +
                        ':regional_indicator_i: - INF\n' +
                        ':regional_indicator_w: - WI\n' +
                        ':regional_indicator_e: - ET\n' +
                        ':regional_indicator_m: - MCD' 
                    )
                    await announcement_message.add_reaction('🇮')
                    await announcement_message.add_reaction('🇼')
                    await announcement_message.add_reaction('🇪')
                    await announcement_message.add_reaction('🇲')
                    if announcement_message:
                        self.announcement_message = announcement_message

        if active == 'stopp':
            return


    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot_user_id:
            return
        guild_announcement_channel = self.bot.get_channel(
            self.guild_announcement_channel_id
        )
        await guild_announcement_channel.send('Soweit so gut')

        



def setup( bot ):
    bot.add_cog( ManualGroups( bot ) )
