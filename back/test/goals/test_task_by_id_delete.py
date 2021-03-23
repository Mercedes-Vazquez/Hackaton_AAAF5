from src.domain.repository.user_repository import UserRepository
from src.domain.repository.goal_repository import GoalRepository
from src.domain.interactor.goal_interactor import GoalInteractor
from src.domain.model.user import hash_password
from src.lib.errors import NotAuthorizedError, BadRequestError, NotFoundError
import pytest


def test_should_delete_the_goal_if_all_data_is_OK_and_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-1");
        
        INSERT INTO goals VALUES
        ("test-goal-id-1", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "test-date", "test-title", "test-category", 1, "user-2");
        """)
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)
    data = {
        "id": "test-id",
        "title": "test-title",
        "description": "test-description",
        "hint": "test-hint",
        "goal_id": "test-goal-id-1"
    }
    goal_interactor.save_task(data)
    tasks = goal_interactor.get_all_tasks_by_goal_id("test-goal-id-1")
    assert len(tasks) == 1
    assert tasks[0].id == "test-id"
    goal_interactor.delete_task_by_id("test-id")
    tasks = goal_interactor.get_all_tasks_by_goal_id("test-goal-id-1")
    assert tasks == []


def test_should_get_NotFoundError_if_the_task_doesnt_exist(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    with pytest.raises(NotFoundError) as exception:
        goal_interactor.delete_task_by_id("task-doesnt-exist")
    assert exception.value.data == {
        "msg": "Task with id 'task-doesnt-exist' not found."
    }


def test_should_get_NotAuthorizedError_if_the_user_is_not_assigned_to_the_admin(database):
    database.executescript(
        """
        INSERT INTO goals VALUES
        ("test-goal-id-1", "2020-03-21", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "2020-03-21", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "2020-03-22", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "2020-03-22", "test-title", "test-category", 1, "user-2");

        INSERT INTO tasks VALUES
        ("test-id-1", "test-title", "test-description", "test-hint", "test-goal-id-1"),
        ("test-id-2", "test-title", "test-description", "test-hint", "test-goal-id-1");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.delete_task_by_id("test-id-1")
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }


def test_should_get_NotAuthorizedError_if_the_admin_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.delete_task_by_id("test-task-id")
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }


def test_should_get_NotAuthorizedError_if_the_user_doesnt_have_an_admin_role(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.delete_task_by_id("test-task-id")
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
