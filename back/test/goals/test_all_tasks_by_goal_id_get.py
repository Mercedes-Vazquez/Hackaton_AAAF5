from src.domain.interactor.goal_interactor import GoalInteractor
from src.domain.repository.goal_repository import GoalRepository
from src.domain.repository.user_repository import UserRepository
from src.lib.errors import NotAuthorizedError, NotFoundError
import pytest


def test_should_get_an_empty_list_if_there_is_no_data_but_exists_the_goal_and_the_user_is_logged(database):
    database.executescript(
        """
        INSERT INTO goals VALUES
        ("test-goal-id-1", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "test-date", "test-title", "test-category", 1, "user-2");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "test-date")
    all_tasks = goal_interactor.get_all_tasks_by_goal_id("test-goal-id-1")
    assert all_tasks == []


def test_should_get_all_tasks_if_there_is_data_and_the_goal_exists_and_the_user_is_logged(database):
    database.executescript(
        """
        INSERT INTO goals VALUES
        ("test-goal-id-1", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "test-date", "test-title", "test-category", 1, "user-2");

        INSERT INTO tasks VALUES
        ("test-id-1", "test-title", "test-description", "test-hint", "test-goal-id-1"),
        ("test-id-2", "test-title", "test-description", "test-hint", "test-goal-id-1");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "test-date")
    all_tasks = goal_interactor.get_all_tasks_by_goal_id("test-goal-id-1")
    assert len(all_tasks) == 2
    assert all_tasks[0].id == "test-id-1"
    assert all_tasks[0].title == "test-title"
    assert all_tasks[0].description == "test-description"
    assert all_tasks[0].hint == "test-hint"
    assert all_tasks[0].goal_id == "test-goal-id-1"


def test_should_raise_NotFoundError_if_the_goal_doesnt_exist_and_the_user_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO goals VALUES
        ("test-id-1", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-id-2", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-id-3", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-id-4", "test-date", "test-title", "test-category", 1, "user-2");

        INSERT INTO tasks VALUES
        ("test-id-1", "test-title", "test-description", "test-hint", "test-goal-id-1"),
        ("test-id-2", "test-title", "test-description", "test-hint", "test-goal-id-1");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "test-date")
    with pytest.raises(NotFoundError) as exception:
        goal_interactor.get_all_tasks_by_goal_id("goal-not-exists")
    assert exception.value.data == {
        "msg": "Goal with id 'goal-not-exists' not found."
    }


def test_should_get_NotAuthorizedError_if_the_user_is_not_logged(database):
    database.executescript(
        """
        INSERT INTO goals VALUES
        ("test-id-1", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-id-2", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-id-3", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-id-4", "test-date", "test-title", "test-category", 1, "user-2");

        INSERT INTO tasks VALUES
        ("test-id-1", "test-title", "test-description", "test-hint", "test-goal-id-1"),
        ("test-id-2", "test-title", "test-description", "test-hint", "test-goal-id-1");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "test-date")
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.get_all_tasks_by_goal_id("test-goal-id-1")
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }
