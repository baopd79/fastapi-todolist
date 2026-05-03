"""
Todo repository : data access layer for Todo model.
all queries filter  by user_id for data isolation"""

from typing import Optional
from app.models.todo import Todo
from sqlmodel import Session, select


class TodoRepository:
    """"""

    def __init__(self, session: Session) -> None:
        self._session = session
    # get_by_id khong filter user_id, tra todo bat ke owner.service check ownership
    #vi repo la data access. khong biet ai request 
    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        return self._session.get(Todo, todo_id)
    # filter user_id la bat buoc vi list scoped by user
    def list_by_user(
        self,
        user_id: int,
        is_completed: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Todo]:
        limit = min(limit, 100)
        statement = select(Todo).where(Todo.user_id == user_id)
        if is_completed is not None:
            statement = statement.where(Todo.is_completed == is_completed)
        statement = statement.order_by(Todo.created_at.desc())
        statement = statement.offset(skip).limit(limit)

        return list(self._session.exec(statement).all())

    def create(self, todo: Todo) -> Todo:
        self._session.add(todo)
        self._session.flush()
        self._session.refresh(todo)
        return todo

    def update(self, todo: Todo, update_data: dict) -> Todo:
        for key, value in update_data.items():
            setattr(todo, key, value)
        self._session.flush()
        self._session.refresh(todo)
        return todo

    def delete(self, todo: Todo) -> None:
        self._session.delete(todo)
        self._session.flush()
