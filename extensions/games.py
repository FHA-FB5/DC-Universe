import discord
import time
import os

from discord.ext import commands
from db import db_session, db_engine, Session

from models.game import Game


class Games(commands.Cog, name='Games'):
    def __init__(self, bot):
        self.bot = bot

        self.guild_games_channel_id = os.getenv(
            'GUILD_GAMES_CHANNEL')
        if isinstance(self.guild_games_channel_id, str):
            self.guild_games_channel_id = int(
                self.guild_games_channel_id)

    @commands.command(aliases=['spiele', 'g'])
    async def games(self, ctx):
        if ctx.channel.id != self.guild_games_channel_id:
            return

        output = ctx.author.mention + " derzeit unterstützen wir folgende Spiele:\n"
        output += '```\n'
        for game in Game.all():
            output += game.key.ljust(8)
            output += f' => {game.name}\n'

        output += '```\n'
        output += "Das erste ist immer der \"key\" gefolgt von dem Namen des Spiels. Mit `!gamejoin` (bzw. kurz `!gj`) gefolgt von einer Auflistung von Keys (Separiert durch Leerzeichen) kannst du dir selbst Spiele zuweisen und mit `!gameleave` (bzw. kurz `!gl`) kannst du diese wieder entfernen."

        # send output
        await ctx.send(output)

    @commands.command(aliases=['gj'])
    async def gamejoin(self, ctx, *game_keys: str):
        success = []
        has = []
        failed = []
        roles = []
        for game_key in game_keys:
            game = Game.getByKey(game_key)
            if (game and game.role):
                role = ctx.guild.get_role(game.role)

                if role in ctx.author.roles:
                    has.append(game_key)
                else:
                    roles.append(role)
                    success.append(game_key)
            else:
                failed.append(game_key)

        await ctx.author.add_roles(*roles)

        # create output embeds
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title='Games'
        )

        if success:
            embed.add_field(
                name='Zugewiesene Spiele:',
                value=', '.join(success), inline=False)

        if has:
            embed.add_field(
                name='Schon zugewiesene Spiele:',
                value=', '.join(has), inline=False)

        if failed:
            embed.add_field(
                name='Nicht zugewiesene Spiele:',
                value=', '.join(failed), inline=False)

        # send embeds
        await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(aliases=['gl'])
    async def gameleave(self, ctx, *game_keys: str):
        success = []
        hasNot = []
        failed = []
        roles = []
        for game_key in game_keys:
            game = Game.getByKey(game_key)
            if (game and game.role):
                role = ctx.guild.get_role(game.role)

                if role in ctx.author.roles:
                    roles.append(role)
                    success.append(game_key)
                else:
                    hasNot.append(game_key)
            else:
                failed.append(game_key)

        await ctx.author.remove_roles(*roles)

        # create output embeds
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title='Games'
        )

        if success:
            embed.add_field(
                name='Verlassene Spiele:',
                value=', '.join(success), inline=False)

        if hasNot:
            embed.add_field(
                name='Nicht vorhandene Spiele:',
                value=', '.join(hasNot), inline=False)

        if failed:
            embed.add_field(
                name='Nicht verlassene Spiele:',
                value=', '.join(failed), inline=False)

        # send embeds
        await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def gameadd(self, ctx, key: str, *name: str):
        # check if game with key exist
        db_game = Game.getByKey(key)

        if not db_game:
            gameName = '{}'.format(' '.join(name))
            db_game = Game()
            db_game.key = key
            db_game.name = gameName
            db_session.add(db_game)

            # commit update
            db_session.commit()

            gameRole = await ctx.guild.create_role(
                name=gameName,
                mentionable=True,
            )

            # get role
            db_game.role = gameRole.id
            db_session.commit()

            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.green(),
                title=f'Spiel angelegt'
            )
            embed.add_field(name="Key", value=f'{key}', inline=False)
            embed.add_field(name="Name", value=f'{gameName}', inline=False)

            Session.close_all()

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)

        else:

            # create output embed
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title=f'Spiel gefunden'
            )
            embed.add_field(
                name="Fehler", value=f'Es wurde das Spiel "{db_game.name}" mit dem Key "{db_game.key}" gefunden.', inline=False)

            # send embed
            await ctx.send(ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))
