import pytest  # type: ignore

from src.domain.repository.user_repository import UserRepository
from src.domain.interactor.user_interactor import UserInteractor

from src.lib.errors import NotAuthorizedError


def test_auth_user_should_return_user_if_password_is_ok(database):
    user_repository = UserRepository(None, database, lambda: "user-1")
    interactor = UserInteractor(None, user_repository)

    user = interactor.auth_user("user-1@example.com", "user-1-password")
    assert user.id == "user-1"
    assert user.username == "user-1@example.com"
    assert user.name == "User 1"
    assert user.is_admin is True


def test_auth_user_should_raise_unauthorized_if_user_is_unknown(database):
    user_repository = UserRepository(None, database, lambda: "user-1")
    interactor = UserInteractor(None, user_repository)

    with pytest.raises(NotAuthorizedError):
        interactor.auth_user("user-unknown@example.com", "user-1-bad-password")


def test_auth_user_should_raise_unauthorized_if_password_not_ok(database):
    user_repository = UserRepository(None, database, lambda: "user-1")
    interactor = UserInteractor(None, user_repository)

    with pytest.raises(NotAuthorizedError):
        interactor.auth_user("user-1@example.com", "user-1-bad-password")
