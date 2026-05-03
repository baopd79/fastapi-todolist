from sqlmodel import Session
from typing import Optional
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreateRequest, TodoUpdateRequest
from app.models.todo import Todo
from app.core.exceptions import ResourceNotFoundError


class TodoService:

    def __init__(self, session: Session) -> None:
        self._session = session
        self._todo_repo = TodoRepository(session)

    def _get_user_todo_or_raise(self, todo_id: int, user_id: int) -> Todo:
        todo = self._todo_repo.get_by_id(todo_id)
        if todo is None or todo.user_id != user_id:
            raise ResourceNotFoundError(f"Todo with id {todo_id} not found")
        return todo

    def create_todo(self, user_id: int, payload: TodoCreateRequest) -> Todo:
        todo = Todo(
            title=payload.title,
            description=payload.description,
            is_completed=False,
            user_id=user_id,
        )
        created = self._todo_repo.create(todo)
        self._session.commit()
        self._session.refresh(created)
        return created

    def list_todos(
        self,
        user_id: int,
        is_completed: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Todo]:
        return self._todo_repo.list_by_user(
            user_id=user_id,
            is_completed=is_completed,
            skip=skip,
            limit=limit,
        )

    def get_todo(self, todo_id: int, user_id: int) -> Todo:
        return self._get_user_todo_or_raise(todo_id, user_id)

    def update_todo(
        self, todo_id: int, user_id: int, payload: TodoUpdateRequest
    ) -> Todo:
        todo = self._get_user_todo_or_raise(todo_id, user_id)
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return todo
        updated = self._todo_repo.update(todo, update_data)
        self._session.commit()
        self._session.refresh(updated)
        return updated

    def delete_todo(self, todo_id: int, user_id: int) -> None:
        todo = self._get_user_todo_or_raise(todo_id, user_id)
        self._todo_repo.delete(todo)
        self._session.commit()
