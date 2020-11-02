from datetime import datetime

from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, Text, PrimaryKeyConstraint, \
    ForeignKeyConstraint
from sqlalchemy.orm import relationship

from db import db_session
from models.base import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    message_id = Column(BigInteger, primary_key=True)
    game_role = Column(BigInteger, nullable=False)
    team_size = Column(Integer, nullable=False)
    team_count = Column(Integer, nullable=False)
    registration_expires = Column(DateTime, nullable=False)
    voice_channel_id = Column(BigInteger, nullable=False)
    text_channel_id = Column(BigInteger, nullable=False)
    role_id = Column(BigInteger, nullable=False)

    teams = relationship("TournamentTeam", back_populates="tournament")

    def __init__(self, message_id: int, game_role_id: int, size: int, count: int, expires: datetime,
                 voice_id: int, text_id: int, role_id: int):
        self.message_id = message_id
        self.game_role = game_role_id
        self.team_size = size
        self.team_count = count
        self.registration_expires = expires
        self.voice_channel_id = voice_id
        self.text_channel_id = text_id
        self.role_id = role_id
        db_session.add(self)

    @classmethod
    def get(cls, message_id: int) -> "Tournament":
        return db_session.query(Tournament).filter(Tournament.message_id == message_id).first()

    @classmethod
    def delete(cls, message_id: int):
        db_session.query(Tournament).filter(Tournament.message_id == message_id).delete()

    def get_team(self, reaction: str) -> "TournamentTeam":
        return db_session.query(TournamentTeam) \
            .filter(TournamentTeam.tournament_message_id == self.message_id) \
            .filter(TournamentTeam.reaction == reaction) \
            .first()

    def add_team(self, reaction: str, voice_id: int, text_id: int, role_id: int) -> "TournamentTeam":
        return TournamentTeam(reaction, self.message_id, voice_id, text_id, role_id)

    def remove_team(self, reaction: str):
        db_session.query(TournamentTeam) \
            .filter(TournamentTeam.reaction == reaction and TournamentTeam.tournament_message_id == self.message_id) \
            .delete()

    def is_player_in_tournament(self, member_id: int) -> bool:
        member = db_session.query(TournamentTeamMember) \
            .join(TournamentTeam, TournamentTeamMember.team_reaction == TournamentTeam.reaction) \
            .join(Tournament, TournamentTeam.tournament_message_id == Tournament.message_id) \
            .filter(TournamentTeamMember.member_id == member_id) \
            .filter(Tournament.message_id == self.message_id).first()
        return member is not None


class TournamentTeam(Base):
    __tablename__ = "tournament_teams"

    reaction = Column(Text, nullable=False)
    tournament_message_id = Column(BigInteger, ForeignKey("tournaments.message_id", ondelete="CASCADE"))
    voice_channel_id = Column(BigInteger, nullable=False)
    text_channel_id = Column(BigInteger, nullable=False)
    role_id = Column(BigInteger, nullable=False)

    PrimaryKeyConstraint(reaction, tournament_message_id)

    members = relationship("TournamentTeamMember", back_populates="team")
    tournament = relationship("Tournament", back_populates="teams")

    def __init__(self, reaction: str, tournament_id: int, voice_id: int, text_id: int, role_id: int):
        self.tournament_message_id = tournament_id
        self.voice_channel_id = voice_id
        self.text_channel_id = text_id
        self.reaction = reaction
        self.role_id = role_id
        db_session.add(self)

    def add_member(self, member_id: int) -> "TournamentTeamMember":
        return TournamentTeamMember(member_id, self.reaction, self.tournament_message_id)

    def remove_member(self, member_id):
        db_session.query(TournamentTeamMember) \
            .filter(TournamentTeamMember.member_id == member_id) \
            .filter(TournamentTeamMember.team_reaction == self.reaction) \
            .delete()

    def has_member(self, member_id) -> bool:
        member = db_session.query(TournamentTeamMember) \
            .filter(TournamentTeamMember.member_id == member_id) \
            .filter(TournamentTeamMember.team_reaction == self.reaction) \
            .first()
        return member is not None


class TournamentTeamMember(Base):
    __tablename__ = "tournament_team_members"

    member_id = Column(BigInteger, nullable=False)
    team_reaction = Column(Text, nullable=False)
    tournament_message_id = Column(BigInteger, nullable=False)

    PrimaryKeyConstraint(member_id, team_reaction, tournament_message_id)
    ForeignKeyConstraint((team_reaction, tournament_message_id),
                         ("tournament_teams.reaction", "tournament_teams.tournament_message_id"),
                         ondelete="CASCADE")

    team = relationship("TournamentTeam", back_populates="members")

    def __init__(self, member_id: int, team_reaction: str, tournament_message_id: int):
        self.member_id = member_id
        self.team_reaction = team_reaction
        self.tournament_message_id = tournament_message_id
        db_session.add(self)
