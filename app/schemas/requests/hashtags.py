from pydantic import BaseModel

class CreateHashtagsRequestSchema(BaseModel):
    post_id:int
    hashtag:str