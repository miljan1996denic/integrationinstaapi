from pydantic import BaseModel

class CreateUsersRequestSchema(BaseModel):
    username: str
    followers_count: int