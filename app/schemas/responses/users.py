import datetime
from pydantic import BaseModel

class CreateUsersResponseSchema(BaseModel):
    id: int
    username: str
    followers_count:int
    created_by: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class GetUsersResponseSchema(CreateUsersResponseSchema, BaseModel):
    pass

class GetAllUsersResponseSchema(CreateUsersResponseSchema, BaseModel):
    pass
