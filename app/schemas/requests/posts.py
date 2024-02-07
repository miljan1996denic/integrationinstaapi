from typing import List
from pydantic import BaseModel

class CreatePostsRequestSchema(BaseModel):
    user_id:int
    permalink:str
    thumbnail_url:str
    caption:str
    like_count:int
    hashtags:List[str]