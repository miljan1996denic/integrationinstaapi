from pydantic import BaseModel

class CreateHashtagsResponseSchema(BaseModel):
    id: int
    post_id:int
    hashtag:str

    class Config:
        orm_mode = True

class GetHashtagsResponseSchema(CreateHashtagsResponseSchema, BaseModel):
    pass

class GetAllHashtagsResponseSchema(CreateHashtagsResponseSchema, BaseModel):
    pass
