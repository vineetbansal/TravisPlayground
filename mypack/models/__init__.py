from sqlalchemy import Column, Integer, Text

from mypack.models.db import Base


class Actor(Base):
    __tablename__ = "actor"

    actor_id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)