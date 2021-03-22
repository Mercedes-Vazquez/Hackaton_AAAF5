from src.domain.interactor.goal_interactor import GoalInteractor
from src.domain.repository.goal_repository import GoalRepository
from src.domain.repository.user_repository import UserRepository
from src.lib.errors import NotAuthorizedError
import pytest


def test_should_get_an_empty_list_if_there_is_no_data_and_the_user_is_logged(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)
    all_goals = goal_interactor.get_all_goals()
    assert all_goals == []


def test_should_get_goals_of_the_day_if_there_is_data_and_the_user_is_logged(database):
    database.executescript(
        f"""
        INSERT INTO goals VALUES
        ("test-id-1", "test-title", "test-category", "test-status", "user-1"),
        ("test-id-2", "test-title", "test-category", "test-status", "user-1"),
        ("test-id-3", "test-title", "test-category", "test-status", "user-1"),
        ("test-id-4", "test-title", "test-category", "test-status", "user-2");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)
    all_goals = goal_interactor.get_all_goals()
    assert len(all_goals) == 3
    assert all_goals[0].id == "test-id-1"
    assert all_goals[0].title == "test-title"
    assert all_goals[0].category == "test-category"
    assert all_goals[0].status == "test-status"
    assert all_goals[0].user_id == "user-1"


def test_should_get_NotAuthorizedError_if_the_user_is_not_logged(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.get_all_goals()
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }
