from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id

from schema.response import ListToDoResponse, ToDoSchema

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

# todo_data = {
#     1: {
#         "id": 1, "contents": "laundry", "is_done": True
#     },
#     2: {
#         "id": 2, "contents": "meal prep", "is_done": False
#     },
#     3: {
#         "id": 3, "contents": "pre-class work", "is_done": False
#     },
# }


@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str | None = None,
        session: Session = Depends(get_db),
):
    todos: List[ToDo] = get_todos(session=session)
    # res = list(todo_data.values())
    if order and order == "DESC":
        # return todos[::-1]
        return ListToDoResponse(
            todos = [ToDoSchema.model_validate(todo) for todo in todos]
        )
    # return todos
    return ListToDoResponse(
        todos = [ToDoSchema.model_validate(todo) for todo in todos]
    )


@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int, session: Session  = Depends(get_db)):
    # todo = todo_data.get(todo_id)
    todo: ToDo | None = get_todo_by_todo_id(session, todo_id)
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")


class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateTodoRequest):
    # todo_data[request.id] = request.model_dump()
    # return todo_data[request.id]


@app.patch("/todos/{todo_id}",status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True)
):
    # todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="Todo Not Found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    # todo = todo_data.pop(todo_id, None)
    # if todo:
    #     return
    raise HTTPException(status_code=404, detail="Todo Not Found")

