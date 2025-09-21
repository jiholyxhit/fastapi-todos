from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import ToDo


def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalar(select(ToDo)))

def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))

def create_todo(session: Session, todo:ToDo):
    session.add(instance = todo)
    session.commit() #DB will automatically create todo id
    session.refresh(instance=todo) #DB read again to update the id info in computer memory
    return todo

def update_todo(session: Session, todo: ToDo):
    session.add(instance = todo)
    session.commit()
    session.refresh(instance = todo)
    return todo


