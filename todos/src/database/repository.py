from typing import List

from fastapi import Depends

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.connection import get_db

from database.orm import ToDo

class ToDoRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session


    def get_todos(self) -> List[ToDo]:
        return list(self.session.scalars(select(ToDo)))


    def get_todo_by_todo_id(self, todo_id: int) -> ToDo:
        return self.session.scalar(select(ToDo).where(ToDo.id == todo_id))


    def create_todo(self, todo:ToDo):
        self.session.add(instance = todo)
        self.session.commit() #DB will automatically create todo id
        self.session.refresh(instance=todo) #DB read again to update the id info in computer memory
        return todo


    def update_todo(self, todo: ToDo):
        self.session.add(instance = todo)
        self.session.commit()
        self.session.refresh(instance = todo)
        return todo


    def delete_todo(self, todo_id: int):
        self.session.execute(delete(ToDo).where(ToDo.id == todo_id))
        self.session.commit()


