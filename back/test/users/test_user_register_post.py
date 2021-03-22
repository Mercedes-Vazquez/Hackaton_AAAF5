from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository
from src.domain.model.user import hash_password
from src.lib.errors import NotAuthorizedError, BadRequestError
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
        user_interactor.register_user(all_fields_missing)
    assert exception.value.data == {
        "id": "REQUIRED",
        "username": "REQUIRED",
        "name": "REQUIRED",
        "password": "REQUIRED",
    }

    id_missing = {
        "username": "test-username",
        "name": "test-name",
        "password": "test-password",
    }
    with pytest.raises(BadRequestError) as exception:
        user_interactor.register_user(id_missing)
    assert exception.value.data == {
        "id": "REQUIRED",
    }

    username_missing = {
        "id": "test-id",
        "name": "test-name",
        "password": "test-password",
    }
    with pytest.raises(BadRequestError) as exception:
        user_interactor.register_user(username_missing)
    assert exception.value.data == {
        "username": "REQUIRED",
    }

    name_missing = {
        "id": "test-id",
        "username": "test-username",
        "password": "test-password",
    }
    with pytest.raises(BadRequestError) as exception:
        user_interactor.register_user(name_missing)
    assert exception.value.data == {
        "name": "REQUIRED",
    }

    password_missing = {
        "id": "test-id",
        "username": "test-username",
        "name": "test-name",
    }
    with pytest.raises(BadRequestError) as exception:
        user_interactor.register_user(password_missing)
    assert exception.value.data == {
        "password": "REQUIRED",
    }


def test_should_register_the_new_user_if_the_request_is_OK_and_the_admin_is_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {
        "id": "test-id",
        "username": "test-username",
        "name": "test-name",
        "password": "test-password",
    }
    user_interactor.register_user(data)
    assigned_users = user_interactor.get_all_assigned_users()
    assert len(assigned_users) == 1
    assert assigned_users[0].id == "test-id"
    assert assigned_users[0].username == "test-username"
    assert assigned_users[0].name == "test-name"
    assert assigned_users[0].password == hash_password("test-password")


def test_should_get_NotAuthorizedError_if_the_admin_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {
        "id": "id",
        "username": "test-username",
        "name": "test-name",
        "password": "test-password",
    }
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.register_user(data)
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
        "id": "id",
        "username": "test-username",
        "name": "test-name",
        "password": "test-password",
    }
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.register_user(data)
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
