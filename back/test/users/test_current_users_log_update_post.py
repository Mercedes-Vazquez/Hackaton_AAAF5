from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository
from src.lib.errors import NotAuthorizedError, BadRequestError
import pytest


def test_should_raise_BadRequestError_if_there_is_not_the_field_timestamp_in_the_request(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {}
    with pytest.raises(BadRequestError) as exception:
        user_interactor.update_current_user_log(data)
    assert exception.value.data == {
        "timestamp": "REQUIRED"
    }


def test_should_raise_BadRequestError_if_the_field_timestamp_isnt_in_iso8601_format_in_the_request(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {
        "timestamp": "timestamp-in-wrong-format"
    }
    with pytest.raises(BadRequestError) as exception:
        user_interactor.update_current_user_log(data)
    assert exception.value.data == {
        "timestamp": "BAD FORMAT"
    }


def test_should_add_a_new_log_entry_if_the_user_is_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {
        "timestamp": "2021-03-04T08:47:19Z"
    }
    user_interactor.update_current_user_log(data)
    log = user_interactor.get_current_users_log()
    assert len(log) == 1


def test_should_get_NotAuthorizedError_if_the_user_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    user_interactor = UserInteractor(None, user_repository)
    data = {
        "timestamp": "2021-03-04T08:47:19Z"
    }
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.update_current_user_log(data)
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }
