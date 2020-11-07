import discord
import os
import typing

from models.pubtour import Pubtourmodel

from discord.ext import commands


class Pubtour(commands.Cog, name='Pubtour'):
    def __init__(self, bot):
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance(self.bot_user_id, str):
            self.bot_user_id = int(self.bot_user_id)
        
        self.guild_tutor_role_id = os.getenv(
            'GUILD_TUTOR_ROLE'
        )
        if isinstance(self.guild_tutor_role_id, str):
            self.guild_tutor_role_id = int(
                self.guild_tutor_role_id
            )


    # all output is just plain text because this command is onetime use only
    @commands.command(aliases=['phase2'], hidden=True)
    @commands.has_permissions(administrator=True)
    async def kneipentour(self, ctx, category: discord.CategoryChannel ):
        guild = ctx.guild
        channel_used = []
        roles_used = []

        if guild.categories.count( category ) >= 1:
            await ctx.send( ctx.author.mention + '\nBeginne mit Prozess.')
            tutor_role = guild.get_role( self.guild_tutor_role_id )

            for c in category.voice_channels:
                channel_used.append( c )

                await ctx.send( ctx.author.mention + f'\nVerarbeite Gruppe: {c.name}')
                name = c.name
                role = await guild.create_role(name=name, hoist=False)
                roles_used.append( role )
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
                    ),
                    tutor_role: discord.PermissionOverwrite(
                        view_channel=True,
                        read_messages=True,
                        connect=True,
                    )
                }
                name = name.lower()
                await c.edit( overwrites=overwrites )
                new_text = await category.create_text_channel( name, overwrites=overwrites )
                channel_used.append( new_text )

                for m in c.members:
                    await m.add_roles( role )

            for c in channel_used:
                Pubtourmodel.set(c.id, True)
            for r in roles_used:
                Pubtourmodel.set(r.id, False)

            await ctx.send( ctx.author.mention + '\nProzess abgeschlossen.')

        else:
            await ctx.send( ctx.author.mention + '\nFehler!' )

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def kneipentour_end(self, ctx):
        context = Pubtourmodel.get()

        for i in context:
            c = None
            if i.is_channel:
                c = ctx.guild.get_channel(i.ctx_id)
            else:
                c = ctx.guild.get_role(i.ctx_id)
            await c.delete()

        Pubtourmodel.delete()
        await ctx.send( ctx.author.mention + '\nDone.')




def setup(bot):
    bot.add_cog(Pubtour(bot))