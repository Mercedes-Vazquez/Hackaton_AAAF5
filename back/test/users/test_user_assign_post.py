from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository
from src.domain.model.user import hash_password
from src.lib.errors import NotAuthorizedError, BadRequestError, NotFoundError
import pytest


def test_should_raise_BadRequestError_if_there_are_not_the_required_fields_in_the_request(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {}
    with pytest.raises(BadRequestError) as exception:
        user_interactor.assign_user(data)
    assert exception.value.data == {
        "user_id": "REQUIRED",
    }


def test_should_raise_NotFoundError_if_the_user_doesnt_exist(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {"user_id": "test-user-doesnt-exist"}
    with pytest.raises(NotFoundError) as exception:
        user_interactor.assign_user(data)
    assert exception.value.data == {
        "msg": "User with id 'test-user-doesnt-exist' not found.",
    }


def test_should_assign_the_user_if_the_request_is_OK_and_the_admin_is_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {"user_id": "user-1"}
    user_interactor.assign_user(data)
    assigned_users = user_interactor.get_all_assigned_users()
    assert len(assigned_users) == 1
    assert assigned_users[0].id == "user-1"


def test_should_get_NotAuthorizedError_if_the_admin_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {"user_id": "test-id"}
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.assign_user(data)
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
    data = {"user_id": "test-id"}
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.assign_user(data)
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
