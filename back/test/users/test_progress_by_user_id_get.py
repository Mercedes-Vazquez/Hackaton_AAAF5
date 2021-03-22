from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository
from src.domain.repository.goal_repository import GoalRepository
from src.lib.errors import NotAuthorizedError, NotFoundError
import pytest


def test_should_get_an_empty_dict_if_there_is_no_data_and_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-1"),
        ("admin-1", "user-2"),
        ("admin-1", "user-3"),
        ("admin-1", "user-4");
        """
    )
    goal_repository = GoalRepository(None, database)
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository, goal_repository)
    progress = user_interactor.get_progress_by_user_id("user-1")
    assert progress == {}


def test_should_get_the_progress_of_the_user_in_each_goal_category_if_there_is_data_and_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-1"),
        ("admin-1", "user-2"),
        ("admin-1", "user-3"),
        ("admin-1", "user-4");

        INSERT INTO goals VALUES
        ("test-goal-id-1", "2020-03-21", "test-title", "test-category-1", 1, "user-1"),
        ("test-goal-id-2", "2020-03-21", "test-title", "test-category-2", 0, "user-1"),
        ("test-goal-id-3", "2020-03-22", "test-title", "test-category-2", 1, "user-1"),
        ("test-goal-id-4", "2020-03-22", "test-title", "test-category-1", 1, "user-2");
        """
    )
    goal_repository = GoalRepository(None, database)
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository, goal_repository)
    progress = user_interactor.get_progress_by_user_id("user-1")
    assert progress["test-category-1"] == (1, 1)
    assert progress["test-category-2"] == (1, 2)


def test_should_get_NotFoundError_if_the_user_doesnt_exist(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    with pytest.raises(NotFoundError) as exception:
        user_interactor.get_progress_by_user_id("user-not-exists")
    assert exception.value.data == {
        "msg": "User with id 'user-not-exists' not found."
    }


def test_should_get_NotAuthorizedError_if_the_admin_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    user_interactor = UserInteractor(None, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.get_progress_by_user_id("user-1")
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }


def test_should_get_NotAuthorizedError_if_the_current_user_doesnt_have_an_admin_role(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.get_progress_by_user_id("user-2")
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }


def test_should_get_NotAuthorizedError_if_the_user_isnt_assigned_to_the_admin(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.get_progress_by_user_id("user-1")
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
