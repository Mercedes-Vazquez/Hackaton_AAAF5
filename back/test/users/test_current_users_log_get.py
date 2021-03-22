from src.domain.interactor.user_interactor import UserInteractor
from src.domain.repository.user_repository import UserRepository
from src.lib.errors import NotAuthorizedError
import pytest


def test_should_get_an_empty_list_if_there_is_no_data_and_the_user_is_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    log = user_interactor.get_current_users_log()
    assert log == []


def test_should_get_the_log_if_there_is_data_and_the_user_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO logs VALUES
        ("2021-03-04T08:47:19Z", "user-1"),
        ("2021-03-04T08:50:23Z", "user-1"),
        ("2021-03-05T08:50:23Z", "user-1"),
        ("2021-03-06T08:50:23Z", "user-1"),
        ("2021-03-06T08:50:23Z", "user-2");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "user-1",
    )
    user_interactor = UserInteractor(None, user_repository)
    log = user_interactor.get_current_users_log()
    assert len(log) == 4
    assert log[0].user_id == "user-1"
    assert log[0].timestamp == "2021-03-04T08:47:19Z"


def test_should_get_NotAuthorizedError_if_the_user_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    user_interactor = UserInteractor(None, user_repository)
    with pytest.raises(NotAuthorizedError) as exception:
        user_interactor.get_current_users_log()
    assert exception.value.data == {
        "msg": "This operation is not authorized. Please, log in."
    }
