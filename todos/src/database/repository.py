from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import ToDo


def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalar(select(ToDo)))

def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo:
    return session.scalar(select(ToDo).where(ToDo.id == todo_id))