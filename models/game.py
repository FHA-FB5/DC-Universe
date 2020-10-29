import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, BigInteger

from db import db_session
from models.base import Base


class Game(Base):
    __tablename__ = 'games'

    key = Column(String(length=255), primary_key=True)
    name = Column(String(length=255))
    role = Column(BigInteger)

    @classmethod
    def getByKey(cls, key: String) -> 'Game':
        return db_session.query(Game).filter(Game.key == key).first()

    @classmethod
    def all(cls) -> List['Game']:
        return db_session.query(Game).all()
