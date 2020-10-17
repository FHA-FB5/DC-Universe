import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, BigInteger, ForeignKey, sql, null

from db import db_session
from models.base import Base

class Speechlist(Base):
    __tablename__ = 'speechlists'

    channel_id = Column(String(length=255), primary_key=True)
    value = Column(Text)

    def __init__(self, channel_id: str):
        self.channel_id = channel_id

    @classmethod
    def get(cls, channel: int) -> 'Speechlist':
        return db_session.query(Speechlist).filter(Speechlist.channel_id == channel).first()
    
    @classmethod
    def set(cls, channel: int, list: str) -> 'Speechlist':
        db_list = Speechlist.get(channel)
        if not db_list:
            db_list = Speechlist(channel)
            db_list.value = str(list)
            db_session.add(db_list)
        else:
            db_list.value = str(list)

        db_session.commit()

        return db_list
    
    @classmethod
    def delete(cls, channel: int) -> 'Speechlist':
        db_session.query(Speechlist).filter(Speechlist.channel_id == channel).delete()
        db_session.commit()