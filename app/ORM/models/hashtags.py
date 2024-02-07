import datetime
from app.ORM.config import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from .posts import PostsModel

class HashtagsModel(Base):
    __tablename__ = 'hashtags'
    
    id = Column(Integer, primary_key=True, index=True)
    hashtags = Column(String, nullable=True)
    post_id = Column(Integer, ForeignKey(PostsModel.id, ondelete="CASCADE"))
    created_by = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)