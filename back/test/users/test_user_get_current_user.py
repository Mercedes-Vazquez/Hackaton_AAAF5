from src.domain.repository.user_repository import UserRepository
from src.domain.interactor.user_interactor import UserInteractor


def test_current_user_should_return_user_if_logged(database):
    def fake_get_user_id():
        return "user-1"

    user_repository = UserRepository(
        None, database, get_current_user_id=fake_get_user_id
    )
    interactor = UserInteractor(None, user_repository)

    user = interactor.get_current_user()
    assert user.id == "user-1"
    assert user.username == "user-1@example.com"
    assert user.name == "User 1"
    assert user.is_admin is True


def test_current_user_should_return_None_if_not_logged(database):
    user_repository = UserRepository(None, database, lambda: None)
    interactor = UserInteractor(None, user_repository)

    assert interactor.get_current_user() is None


def test_current_user_should_return_None_if_not_id_getter_function(database):
    user_repository = UserRepository(None, database)
    interactor = UserInteractor(None, user_repository)

    assert interactor.get_current_user() is None
