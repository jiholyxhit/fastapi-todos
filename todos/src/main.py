from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.request import CreateToDoRequest

from schema.response import ToDoListSchema, ToDoSchema

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

# todo_data = {
#     1: {q
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
        return ToDoListSchema(
            todos = [ToDoSchema.model_validate(todo) for todo in todos[::-1]]
        )
    # return todos
    return ToDoListSchema(
        todos = [ToDoSchema.model_validate(todo) for todo in todos]
    )


@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id: int, session: Session  = Depends(get_db)):
    # todo = todo_data.get(todo_id)
    todo: ToDo | None = get_todo_by_todo_id(session, todo_id)
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")


@app.post("/todos", status_code=201)
def create_todo_handler(
        request: CreateToDoRequest,
        session: Session  = Depends(get_db),
):
    todo: ToDo = ToDo.create(request=request) #make an ORM model obj made with req schema
    todo: ToDo = create_todo(session = session, todo = todo) #pass the ORM model obj to DB through repository function and then refresh to return back
    return ToDoSchema.model_validate(todo)
    # return todo_data[request.id]


@app.patch("/todos/{todo_id}",status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session = session, todo_id = todo_id)
    if todo:
        todo.done() if is_done else todo.undone() #Python ternary expression
        todo: ToDo = update_todo(session = session, todo = todo)
        return ToDoSchema.model_validate(todo)
    # todo = todo_data.get(todo_id)
    # if todo:
        # todo["is_done"] = is_done
        # return todo
    raise HTTPException(status_code=404, detail="Todo Not Found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session = session, todo_id = todo_id)
    if not todo:
        raise HTTPException(status_code = 404, detail = "ToDo Not Found")
    delete_todo(session = session, todo_id = todo_id)
    # todo = todo_data.pop(todo_id, None)
    # if todo:
    #     return
    #raise HTTPException(status_code=404, detail="Todo Not Found")

