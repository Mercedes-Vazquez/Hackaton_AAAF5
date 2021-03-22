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
    all_goals = goal_interactor.get_current_users_daily_goals()
    assert all_goals == []


def test_should_get_goals_of_the_day_if_there_is_data_and_the_user_is_logged(database):
    database.executescript(
        """
        INSERT INTO goals VALUES
        ("test-id-1", "test-date-1", "test-title", "test-category", 1, "user-1"),
        ("test-id-2", "test-date-1", "test-title", "test-category", 1, "user-1"),
        ("test-id-3", "test-date-1", "test-title", "test-category", 1, "user-1"),
        ("test-id-4", "test-date-2", "test-title", "test-category", 0, "user-1"),
        ("test-id-5", "test-date", "test-title", "test-category", 1, "user-2");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "test-date-1")
    all_goals = goal_interactor.get_current_users_daily_goals()
    assert len(all_goals) == 3
    assert all_goals[0].id == "test-id-1"
    assert all_goals[0].date == "test-date-1"
    assert all_goals[0].title == "test-title"
    assert all_goals[0].category == "test-category"
    assert all_goals[0].status == 1
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
        goal_interactor.get_current_users_daily_goals()
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }
