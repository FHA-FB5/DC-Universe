import json
import os

from typing import List

from sqlalchemy import Column, String, Boolean, Text

from db import db_session
from models.base import Base


class State(Base):
    __tablename__ = 'states'

    name = Column(String(length=255), primary_key=True)
    value = Column(Text)

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def get(cls, name: str) -> 'State':
        return db_session.query(State).filter(State.name == name).first()

    @classmethod
    def set(cls, name: str, value) -> 'State':
        db_state = State.get(name)
        if not db_state:
            db_state.name = name
            db_state.value = str(value)
            db_session.add(db_state)
        else:
            db_state.value = str(value)

        db_session.commit()

        return db_state

    @classmethod
    def delete(cls, name: str):
        db_session.query(State).filter(State.name == name).first().delete()
        db_session.commit()
