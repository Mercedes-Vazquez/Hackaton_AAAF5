from src.domain.repository.user_repository import UserRepository
from src.domain.repository.goal_repository import GoalRepository
from src.domain.interactor.goal_interactor import GoalInteractor
from src.domain.model.user import hash_password
from src.lib.errors import NotAuthorizedError, BadRequestError, NotFoundError
import pytest


def test_should_get_an_empty_list_if_there_is_no_data_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-1"),
        ("admin-1", "user-2"),
        ("admin-1", "user-3");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "2020-03-21")
    goals = goal_interactor.get_goals_by_date_and_assigned_user_id(
        "2020-03-21", "user-1")
    assert goals == []


def test_should_get_the_goals_if_there_is_data_and_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-1"),
        ("admin-1", "user-2"),
        ("admin-1", "user-3");
        
        INSERT INTO goals VALUES
        ("test-goal-id-1", "2020-03-21", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "2020-03-21", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "2020-03-22", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "2020-03-22", "test-title", "test-category", 1, "user-2");
        
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "2020-03-21")
    goals = goal_interactor.get_goals_by_date_and_assigned_user_id(
        "2020-03-21", "user-1")
    assert len(goals) == 2
    assert goals[0].id == "test-goal-id-1"
    assert goals[0].date == "2020-03-21"
    assert goals[0].title == "test-title"
    assert goals[0].category == "test-category"
    assert goals[0].status == 1
    assert goals[0].user_id == "user-1"


def test_should_get_BadRequestError_if_the_date_isnt_in_iso8601_format(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "2020-03-21")
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.get_goals_by_date_and_assigned_user_id(
            "date-with-wrong-format", "user-1")
    assert exception.value.data == {
        "date": "BAD FORMAT"
    }


def test_should_get_NotAuthorizedError_if_the_user_is_not_assigned_to_the_admin(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository, get_current_date=lambda: "2020-03-21")
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.get_goals_by_date_and_assigned_user_id(
            "2020-03-21", "user-1")
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
        None, goal_repository, user_repository, get_current_date=lambda: "test-date")
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.get_goals_by_date_and_assigned_user_id(
            "test-date", "test-user-id")
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
        None, goal_repository, user_repository, get_current_date=lambda: "test-date")
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.get_goals_by_date_and_assigned_user_id(
            "test-date", "test-user-id")
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
