import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, BigInteger, ForeignKey, sql, null

from db import db_session
from models.base import Base


class Groupphaseuser(Base):
    __tablename__ = 'groupphase_users'

    id = Column(BigInteger, primary_key=True)
    groupID = Column(Integer)

    def __init__(self, id: str):
        self.id = id

    @classmethod
    def get(cls, id: int) -> 'Groupphaseuser':
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.id == id).first()

    @classmethod
    def set(cls, id: int) -> 'Groupphaseuser':
        db_Groupphaseuser = Groupphaseuser.get(id)
        if not db_Groupphaseuser:
            db_Groupphaseuser = Groupphaseuser(id)
            db_session.add(db_Groupphaseuser)
            db_session.commit()

        return db_Groupphaseuser

    @classmethod
    def delete(cls, id: int):
        db_session.query(Groupphaseuser).filter(
            Groupphaseuser.id == id).delete()
        db_session.commit()

    @classmethod
    def all(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).all()

    @classmethod
    def deleteall(cls):
        db_session.query(Groupphaseuser).delete()
        db_session.commit()
