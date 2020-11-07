import json
import os
from typing import List

from sqlalchemy import Column, String, Boolean, Text, Integer, BigInteger, ForeignKey, sql, null

from db import db_session
from models.base import Base

class Pubtourmodel(Base):
    __tablename__ = 'pubs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ctx_id = Column(BigInteger, nullable=False)
    is_channel = Column(Boolean, nullable=False)

    def __init__(self, ctx: int, b: bool):
        self.ctx_id = ctx
        self.is_channel = b

    @classmethod
    def set(cls, ctx: int, b: bool):
        new = Pubtourmodel(ctx, b)
        db_session.add(new)
        db_session.commit()
        return new

    @classmethod
    def get(cls) -> List['Pubtourmodel']:
        return db_session.query(Pubtourmodel).all()

    @classmethod
    def delete(cls):
        db_session.query(Pubtourmodel).delete()
        db_session.commit()