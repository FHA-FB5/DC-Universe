import discord
import os

from discord.ext import commands

class Error(commands.Cog, name='Error'):
    def __init__(self, bot):
        self.bot = bot

        self.guild_error_channel_id = os.getenv(
            'GUILD_ERROR_CHANNEL'
        )
        if isinstance(self.guild_error_channel_id, str):
            self.guild_error_channel_id = int(
                self.guild_error_channel_id
            )

        self.debug_role_id = os.getenv(
            'GUILD_DEBUG_ROLE'
        )
        if isinstance(self.debug_role_id, str):
            self.debug_role_id = int(
                self.debug_role_id
            )

    @commands.Cog.listener()
    async def on_command_error( self, ctx, err ):
        channel = self.bot.get_channel(
                self.guild_error_channel_id
            )

        debug = discord.utils.get( ctx.guild.roles, id=self.debug_role_id )
        
        msg = f'{debug.mention}\n```' + str(err) + f'\n```ausgelöst in {ctx.channel.mention} durch {ctx.author.mention}'
        await channel.send( msg )

def setup(bot):
    bot.add_cog(Error(bot))
