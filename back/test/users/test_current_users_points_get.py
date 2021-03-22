from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository
from src.domain.repository.goal_repository import GoalRepository
from src.lib.errors import NotAuthorizedError
import pytest


def test_should_get_zero_if_there_are_not_completed_tasks_and_the_user_is_logged_in(database):
    goal_repository = GoalRepository(None, database)
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository, goal_repository)
    points = user_interactor.get_current_users_points()
    assert points == 0


def test_should_get_two_points_for_each_completed_task_if_the_user_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO goals VALUES
        ("test-goal-id-1", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "test-date", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "test-date", "test-title", "test-category", 1, "user-2");

        INSERT INTO tasks VALUES
        ("test-id-1", "test-title", "test-description", "test-hint", "test-goal-id-1"),
        ("test-id-2", "test-title", "test-description", "test-hint", "test-goal-id-1"),
        ("test-id-3", "test-title", "test-description", "test-hint", "test-goal-id-2"),
        ("test-id-4", "test-title", "test-description", "test-hint", "test-goal-id-3"),
        ("test-id-5", "test-title", "test-description", "test-hint", "test-goal-id-4");
        """
    )
    goal_repository = GoalRepository(None, database)
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository, goal_repository)
    points = user_interactor.get_current_users_points()
    assert points == 4


def test_should_get_NotAuthorizedError_if_the_user_is_not_logged_in(database):
    goal_repository = GoalRepository(None, database)
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    user_interactor = UserInteractor(None, user_repository, goal_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.get_current_users_points()
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }
