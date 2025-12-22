from typing import List

from fastapi import Depends, HTTPException, Body, APIRouter
from sqlalchemy.orm import Session

from security import get_access_token

from service.user import UserService

from database.connection import get_db
from database.orm import ToDo, User
from database.repository import ToDoRepository, UserRepository
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema

router = APIRouter(prefix = "/todos")


@router.get("", status_code=200)
def get_todos_handler(
        access_token: str = Depends(get_access_token),
        order: str | None = None, #query string / default None
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
) -> ToDoListSchema:
    username: str = user_service.decode_jwt(access_token=access_token)

    user: User | None = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    todos: List[ToDo] = user.todos #User ORM relationship eager loading

    if order and order == "DESC":
        return ToDoListSchema(
            todos = [ToDoSchema.model_validate(todo) for todo in todos[::-1]]
        )
    # return todos
    return ToDoListSchema(
        todos = [ToDoSchema.model_validate(todo) for todo in todos]
    )


@router.get("/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int, todo_repo: ToDoRepository = Depends(),):
    # todo = todo_data.get(todo_id)
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id)
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")


@router.post("", status_code=201)
def create_todo_handler(
        request: CreateToDoRequest,
        todo_repo: ToDoRepository = Depends(),
):
    todo: ToDo = ToDo.create(request=request) #make an ORM model obj made with req schema
    todo: ToDo = todo_repo.create_todo(todo = todo) #pass the ORM model obj to DB through repository function and then refresh to return back
    return ToDoSchema.model_validate(todo)
    # return todo_data[request.id]


@router.patch("/{todo_id}",status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        todo_repo: ToDoRepository = Depends(),
):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id = todo_id)
    if todo:
        todo.done() if is_done else todo.undone() #Python ternary expression
        todo: ToDo = todo_repo.update_todo(todo = todo)
        return ToDoSchema.model_validate(todo)
    # todo = todo_data.get(todo_id)
    # if todo:
        # todo["is_done"] = is_done
        # return todo
    raise HTTPException(status_code=404, detail="Todo Not Found")


@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        todo_repo: ToDoRepository = Depends(),
):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id = todo_id)
    if not todo:
        raise HTTPException(status_code = 404, detail = "ToDo Not Found")
    todo_repo.delete_todo(todo_id = todo_id)
