from typing import List

from pydantic import BaseModel, ConfigDict

class ToDoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contents: str
    is_done: bool

    # class Config:
    #     orm_mode = True


class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class JWTResponse(BaseModel):
    access_token: str

