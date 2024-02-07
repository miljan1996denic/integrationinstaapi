import datetime
from app.ORM.config import Base
from sqlalchemy import Column, String, Integer, DateTime

class UsersModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    followers_count = Column(Integer, nullable=True)
    created_by = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

