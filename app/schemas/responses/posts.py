import datetime
from typing import List
from pydantic import BaseModel

class CreatePostsResponseSchema(BaseModel):
    id: int
    user_id:int
    permalink:str
    thumbnail_url:str
    caption:str
    like_count:int
    hashtags:List[str]
    created_by: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class GetPostsResponseSchema(CreatePostsResponseSchema, BaseModel):
    pass

class GetAllPostsResponseSchema(CreatePostsResponseSchema, BaseModel):
    pass
