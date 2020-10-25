import json
import os
from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, BigInteger, ForeignKey, sql, null

from db import db_session
from models.base import Base

class Speechlistmodel(Base):
    __tablename__ = 'speechlists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger, nullable=False)
    member_id = Column(BigInteger, nullable=False)
    member_name = Column(String(length=255))
    prio = Column(Boolean, default=False)

    def __init__(self, channel: int, member: int, name: str, prio: bool):
        self.channel_id = channel
        self.member_id = member
        self.member_name = name
        self.prio = prio

    @classmethod
    def get(cls, channel: int, member: int) -> 'Speechlistmodel':
        return db_session.query(Speechlistmodel).filter(Speechlistmodel.channel_id == channel, Speechlistmodel.member_id == member).first()
    
    @classmethod
    def all(cls, channel: int) -> List['Speechlistmodel']:
        return db_session.query(Speechlistmodel).filter(Speechlistmodel.channel_id == channel).order_by(Speechlistmodel.prio.asc(), Speechlistmodel.id.asc()).all()

    @classmethod
    def set(cls, channel: int, member: int, name: str, prio: bool) -> 'Speechlistmodel':
        db_list = Speechlistmodel.get(channel, member)
        if not db_list:
            db_list = Speechlistmodel(channel, member, name, prio)
            db_session.add(db_list)
        else:
            db_list.name = name
            db_list.prio = prio

        db_session.commit()

        return db_list
    
    @classmethod
    def deleteAll(cls, channel: int):
        db_session.query(Speechlistmodel).filter(Speechlistmodel.channel_id == channel).delete()
        db_session.commit()
    
    @classmethod
    def delete(cls, channel: int, member: int):
        db_session.query(Speechlistmodel).filter(Speechlistmodel.channel_id == channel, Speechlistmodel.member_id == member).delete()
        db_session.commit()