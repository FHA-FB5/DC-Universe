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

    def __init__(self, name: str, role: int, voiceChannel: int, textChannel: int):
        self.name = name
        self.role = role
        self.voiceChannel = voiceChannel
        self.textChannel = textChannel

    @classmethod
    def all(cls) -> List['Group']:
        return db_session.query(Group).all()

    @classmethod
    def delete(cls, id: int):
        db_session.query(Group).filter(
            Group.id == id).delete()
        db_session.commit()
