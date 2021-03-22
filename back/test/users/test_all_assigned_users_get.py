from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository
from src.lib.errors import NotAuthorizedError
import pytest


def test_should_get_an_empty_list_if_there_is_no_data_and_the_admin_is_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    assigned_users = user_interactor.get_all_assigned_users()
    assert assigned_users == []


def test_should_get_all_the_assigned_users_if_there_is_data_and_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-1"),
        ("admin-1", "user-2"),
        ("admin-1", "user-3"),
        ("admin-1", "user-4");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    assigned_users = user_interactor.get_all_assigned_users()
    assert len(assigned_users) == 4
    assert assigned_users[0].id == "user-1"
    assert assigned_users[0].username == "user-1@example.com"


def test_should_get_NotAuthorizedError_if_the_admin_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    user_interactor = UserInteractor(None, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.get_all_assigned_users()
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }


def test_should_get_NotAuthorizedError_if_the_user_doesnt_have_an_admin_role(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.get_all_assigned_users()
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
