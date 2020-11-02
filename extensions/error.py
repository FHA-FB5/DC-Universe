import discord
import os
import math

from discord.ext import commands

from extensions.util import create_embed, EmbedColour

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
    async def on_command_error(self, ctx, err):
        channel = self.bot.get_channel(
            self.guild_error_channel_id
        )
        debug = discord.utils.get(ctx.guild.roles, id=self.debug_role_id)

        if isinstance( err, commands.MissingAnyRole ):
            embed = await create_embed( 'Du hst nicht die benötigten Rechte für diesen Befehl!\nVersuche es nächstes Jahr noch einmal, wenn deine vielversprechende Tutorenbewerbung angenommen worden ist :)',
                                            EmbedColour.ERROR )

            await ctx.send(ctx.author.mention, embed=embed)

        if isinstance( err, commands.MissingPermissions ):
            embed = await create_embed( 'Dieser Befehl kann nur von Admins ausgeführt werden!',
                                            EmbedColour.ERROR )

            await ctx.send(ctx.author.mention, embed=embed)
        
        if isinstance( err, commands.CommandOnCooldown ):
            embed = await create_embed( 'Dieser Befehl hat noch Cooldown, bitte warte weitere {}s'.format( math.ceil( err.retry_after ) ) ,
                                            EmbedColour.ERROR )

            await ctx.send(ctx.author.mention, embed=embed)

        # create output embed
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title=f'Ein Fehler ist aufgetreten!'
        )
        embed.add_field(
            name="Channel", value=f'{ctx.channel.mention}', inline=False)
        embed.add_field(
            name="Author", value=f'{ctx.author.mention}', inline=False)

        embed.add_field(
            name="Nachricht", value=f'{ctx.message.content}', inline=False)

        embed.add_field(
            name="Link", value=f'{ctx.message.jump_url}', inline=False)

        embed.add_field(name="Fehler", value="{}: {}".format(
            type(err).__name__, err), inline=False)

        # send embed
        await channel.send(debug.mention, embed=embed)


def setup(bot):
    bot.add_cog(Error(bot))
