"""Todo CRUD API routes
All endpoints require authentication(CurrentUserDep)
Ownership is enforced at the service layer"""

from fastapi import APIRouter, status, Query
from typing import Optional
from app.schemas.todo import TodoCreateRequest, TodoResponse, TodoUpdateRequest
from app.core.deps import CurrentUserDep, TodoServiceDep

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new todo",
)
def create_todo(
    payload: TodoCreateRequest,
    current_user: CurrentUserDep,
    todo_service: TodoServiceDep,
) -> TodoResponse:
    todo = todo_service.create_todo(current_user.id, payload)
    return TodoResponse.model_validate(todo)


@router.get("", response_model=list[TodoResponse], summary="List todo for current user")
def list_todos(
    current_user: CurrentUserDep,
    todo_service: TodoServiceDep,
    is_completed: Optional[bool] = Query(
        default=None, description="Filter by completion status"
    ),
    skip: int = Query(default=0, ge=0, description="Number of items to skio"),
    limit: int = Query(default=20, ge=1, le=100, description="Max items to return"),
) -> list[TodoResponse]:
    todos = todo_service.list_todos(
        user_id=current_user.id,
        is_completed=is_completed,
        skip=skip,
        limit=limit,
    )
    return [TodoResponse.model_validate(t) for t in todos]


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Get a specific todo",
)
def get_todo(
    todo_id: int,
    current_user: CurrentUserDep,
    todo_service: TodoServiceDep,
) -> TodoResponse:
    todo = todo_service.get_todo(todo_id, current_user.id)
    return TodoResponse.model_validate(todo)


@router.patch(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="update a todo(partial)",
)
def update_todo(
    todo_id: int,
    payload: TodoUpdateRequest,
    current_user: CurrentUserDep,
    todo_service: TodoServiceDep,
) -> TodoResponse:
    todo = todo_service.update_todo(todo_id, current_user.id, payload)
    return TodoResponse.model_validate(todo)

@router.delete("/{todo_id}",status_code=status.HTTP_204_NO_CONTENT,summary="Delete a todo",)
def delete_todo(
    todo_id:int,
    current_user: CurrentUserDep,
    todo_service : TodoServiceDep,
)-> None:
    todo_service.delete_todo(todo_id, current_user.id)