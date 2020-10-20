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
    course = Column(String(length=255))

    def __init__(self, id: str):
        self.id = id

    @classmethod
    def get(cls, id: int) -> 'Groupphaseuser':
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.id == id).first()

    @classmethod
    def set(cls, id: int, course: str) -> 'Groupphaseuser':
        db_Groupphaseuser = Groupphaseuser.get(id)
        if not db_Groupphaseuser:
            db_Groupphaseuser = Groupphaseuser(id)
            db_Groupphaseuser.course = course
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
    def inf(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.course == "inf").all()

    @classmethod
    def wi(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.course == "wi").all()

    @classmethod
    def et(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.course == "et").all()

    @classmethod
    def mcd(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.course == "mcd").all()

    @classmethod
    def allWithoutGroup(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.groupID == sql.null()).all()

    @classmethod
    def allWithoutGroupInf(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.course == "inf").filter(Groupphaseuser.groupID == sql.null()).all()

    @classmethod
    def allWithoutGroupWi(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.course == "wi").filter(Groupphaseuser.groupID == sql.null()).all()

    @classmethod
    def allWithoutGroupEt(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.course == "et").filter(Groupphaseuser.groupID == sql.null()).all()

    @classmethod
    def allWithoutGroupMcd(cls) -> List['Groupphaseuser']:
        return db_session.query(Groupphaseuser).filter(Groupphaseuser.course == "mcd").filter(Groupphaseuser.groupID == sql.null()).all()

    @classmethod
    def deleteall(cls):
        db_session.query(Groupphaseuser).delete()
        db_session.commit()
