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

    all_fields_missing = {}
    with pytest.raises(BadRequestError) as exception:
        user_interactor.update_user_profile("test-id", all_fields_missing)
    assert exception.value.data == {
        "username": "REQUIRED",
        "name": "REQUIRED",
        "password": "REQUIRED",
    }

    username_missing = {
        "name": "test-name",
        "password": "test-password",
    }
    with pytest.raises(BadRequestError) as exception:
        user_interactor.update_user_profile("test-id", username_missing)
    assert exception.value.data == {
        "username": "REQUIRED",
    }

    name_missing = {
        "username": "test-username",
        "password": "test-password",
    }
    with pytest.raises(BadRequestError) as exception:
        user_interactor.update_user_profile("test-id", name_missing)
    assert exception.value.data == {
        "name": "REQUIRED",
    }

    password_missing = {
        "username": "test-username",
        "name": "test-name",
    }
    with pytest.raises(BadRequestError) as exception:
        user_interactor.update_user_profile("test-id", password_missing)
    assert exception.value.data == {
        "password": "REQUIRED",
    }


def test_should_raise_NotFoundError_if_the_user_doesnt_exist(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {
        "username": "test-username",
        "name": "test-name",
        "password": "test-password",
    }
    with pytest.raises(NotFoundError) as exception:
        user_interactor.update_user_profile("test-user-doesnt-exist", data)
    assert exception.value.data == {
        "msg": "User with id 'test-user-doesnt-exist' not found.",
    }


def test_should_update_the_user_if_the_request_is_OK_and_the_admin_is_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {
        "username": "test-username",
        "name": "test-name",
        "password": "test-password",
    }
    user_interactor.update_user_profile("user-1", data)
    user = user_interactor.get_user_by_id("user-1")
    assert user.id == "user-1"
    assert user.username == "test-username"
    assert user.name == "test-name"
    assert user.password == hash_password("test-password")


def test_should_get_NotAuthorizedError_if_the_admin_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {
        "username": "test-username",
        "name": "test-name",
        "password": "test-password",
    }
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.update_user_profile("test-id", data)
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
    data = {
        "username": "test-username",
        "name": "test-name",
        "password": "test-password",
    }
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.update_user_profile("test-id", data)
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
