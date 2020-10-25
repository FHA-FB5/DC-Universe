import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, BigInteger

from db import db_session
from models.base import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=255))
    role = Column(BigInteger)
    voiceChannel = Column(BigInteger)
    textChannel = Column(BigInteger)
    course = Column(String(length=255))

    def __init__(self, name: str, role: int, voiceChannel: int, textChannel: int):
        self.name = name
        self.role = role
        self.voiceChannel = voiceChannel
        self.textChannel = textChannel

    @classmethod
    def get(cls, id: int) -> 'Group':
        return db_session.query(Group).filter(Group.id == id).first()

    @classmethod
    def getByTextChannelId(cls, textChannel: int) -> 'Group':
        return db_session.query(Group).filter(Group.textChannel == textChannel).first()

    @classmethod
    def all(cls) -> List['Group']:
        return db_session.query(Group).all()

    @classmethod
    def inf(cls) -> List['Group']:
        return db_session.query(Group).filter(Group.course == "inf").all()

    @classmethod
    def wi(cls) -> List['Group']:
        return db_session.query(Group).filter(Group.course == "wi").all()

    @classmethod
    def et(cls) -> List['Group']:
        return db_session.query(Group).filter(Group.course == "et").all()

    @classmethod
    def mcd(cls) -> List['Group']:
        return db_session.query(Group).filter(Group.course == "mcd").all()

    @classmethod
    def delete(cls, id: int):
        db_session.query(Group).filter(
            Group.id == id).delete()
        db_session.commit()
