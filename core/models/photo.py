from sqlalchemy import Column, Integer, Text
from sqlalchemy.sql.schema import ForeignKey

from core.db import db


class PhotoModel(db.Model):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    url = Column(Text)
    description = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
