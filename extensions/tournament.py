from datetime import datetime, timedelta

import discord
from discord.ext import commands

from db import db_session
from extensions.util import remove_reaction, create_role_and_channels
from models.tournament import Tournament


class Tournaments(commands.Cog, name="Tournaments"):

    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.command()
    async def tournament(self, ctx, role: discord.Role, team_size: int, team_count: int, period: int = 15):
        expires = datetime.now() + timedelta(minutes=period)
        embed = discord.Embed(
            color=discord.Color.blue(),
            title=f"A new {role.name} Tournament was started",
        )
        embed.add_field(name="Teams",
                        value=f"This tournament will have {team_size} member(s) per team "
                              f"and a maximum of {team_count} teams.")
        embed.add_field(name="Registration",
                        value=f"If you want to enter a new team react with a new Reaction.\n"
                              f"If you want to enter an existing team click in its Reaction.\n"
                              f"To exit a team remove your Reaction.")
        embed.add_field(name="Deadline",
                        value=f"Registration will be closed when {team_count} **full** teams are formed\n"
                              f"OR\n"
                              f"at {expires:%H:%M}.")
        msg = await ctx.send(embed=embed)
        role, voice, text = await create_role_and_channels(ctx.guild, f"{role.name} Tournament Participant",
                                                           f" {role.name} Tournament")
        Tournament(message_id=msg.id, game_role_id=role.id, size=team_size, count=team_count, expires=expires,
                   voice_id=voice.id, text_id=text.id, role_id=role.id)
        db_session.commit()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event: discord.RawReactionActionEvent):
        tournament = Tournament.get(event.message_id)
        if tournament is None:
            return
        guild = self.guild(event.guild_id)
        if tournament.is_player_in_tournament(event.user_id):
            await remove_reaction(guild, event)
            return
        tournament_role = guild.get_role(tournament.role_id)
        reaction = event.emoji.name
        team = tournament.get_team(reaction)
        team_role: discord.Role = None
        if team is None:
            team_role, voice, text = await create_role_and_channels(guild, f"Team {reaction} Member",
                                                                    f"Team {reaction}")
            team = tournament.add_team(reaction=reaction, voice_id=voice.id, text_id=text.id, role_id=team_role.id)
        if team_role is None:
            team_role = guild.get_role(team.role_id)
        if len(team.members) >= tournament.team_size:
            await remove_reaction(guild, event)
            return
        await event.member.add_roles(tournament_role, team_role)
        team.add_member(event.user_id)
        db_session.commit()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event: discord.RawReactionActionEvent):
        tournament = Tournament.get(event.message_id)
        if tournament is None:
            return
        team = tournament.get_team(event.emoji.name)
        if team is None:
            return
        if not team.has_member(event.user_id):
            return
        guild = self.guild(event.guild_id)
        member: discord.Member = guild.get_member(event.user_id)
        tournament_role: discord.Role = guild.get_role(tournament.role_id)
        team_role = guild.get_role(team.role_id)
        await member.remove_roles(tournament_role, team_role)
        team.remove_member(event.user_id)
        if len(team.members) == 0:
            await guild.get_channel(team.voice_channel_id).delete()
            await guild.get_channel(team.text_channel_id).delete()
            await team_role.delete()
            tournament.remove_team(team.reaction)
        db_session.commit()

    @commands.Cog.listener()
    async def on_raw_message_edit(self, event: discord.RawMessageUpdateEvent):
        tournament = Tournament.get(event.message_id)
        if tournament is None:
            return
        if len(event.data["embeds"]) > 0:
            return
        guild = self.guild(int(event.data["guild_id"]))
        await guild.get_channel(tournament.voice_channel_id).delete()
        await guild.get_channel(tournament.text_channel_id).delete()
        await guild.get_role(tournament.role_id).delete()
        for team in tournament.teams:
            await guild.get_channel(team.voice_channel_id).delete()
            await guild.get_channel(team.text_channel_id).delete()
            await guild.get_role(team.role_id).delete()
        Tournament.delete(event.message_id)
        db_session.commit()

    def guild(self, guild_id: int) -> discord.Guild:
        return self.bot.get_guild(guild_id)


def setup(bot):
    bot.add_cog(Tournaments(bot))
