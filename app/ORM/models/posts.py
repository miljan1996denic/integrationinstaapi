import datetime
from app.ORM.config import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from .users import UsersModel

class PostsModel(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    permalink = Column(String, unique=True, index=True, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    caption = Column(String, nullable=True)
    like_count = Column(Integer, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey(UsersModel.id, ondelete="CASCADE"))
    created_by = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)