from src.domain.repository.user_repository import UserRepository
from src.domain.repository.goal_repository import GoalRepository
from src.domain.interactor.goal_interactor import GoalInteractor
from src.domain.model.user import hash_password
from src.lib.errors import NotAuthorizedError, BadRequestError, NotFoundError
import pytest


def test_should_create_the_goal_if_the_goal_doesnt_exist_and_all_data_is_OK_and_the_admin_is_logged_in(database):
    database.executescript(
        "INSERT INTO admin_users VALUES('admin-1', 'user-1');")
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)
    data = {
        "id": "test-id",
        "date": "2020-03-15",
        "title": "test-title",
        "category": "test-category",
        "status": 0,
        "user_id": "user-1"
    }
    goal_interactor.save_assigned_users_goal(data)
    goals = goal_interactor.get_goals_by_date_and_assigned_user_id(
        "2020-03-15", "user-1")
    assert len(goals) == 1
    assert goals[0].id == "test-id"
    assert goals[0].date == "2020-03-15"
    assert goals[0].title == "test-title"
    assert goals[0].category == "test-category"
    assert goals[0].status == False
    assert goals[0].user_id == "user-1"


def test_should_update_the_goal_if_the_goal_exists_and_all_data_is_OK_and_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ('admin-1', 'user-1');
        
        INSERT INTO goals VALUES
        ("test-id-1", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-id-2", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-id-3", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-id-4", "2020-03-16", "test-title", "test-category", 0, "user-1"),
        ("test-id-5", "2020-03-17", "test-title", "test-category", 1, "user-2");
        """)
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)
    data = {
        "id": "test-id-1",
        "date": "2020-03-18",
        "title": "test-title",
        "category": "test-category",
        "status": 0,
        "user_id": "user-1"
    }
    goal_interactor.save_assigned_users_goal(data)
    goals = goal_interactor.get_goals_by_date_and_assigned_user_id(
        "2020-03-18", "user-1")
    assert len(goals) == 1
    assert goals[0].id == "test-id-1"
    assert goals[0].date == "2020-03-18"
    assert goals[0].title == "test-title"
    assert goals[0].category == "test-category"
    assert goals[0].status == False
    assert goals[0].user_id == "user-1"


def test_should_raise_BadRequestError_if_there_are_not_the_required_fields_in_the_request(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)

    all_fields_missing = {}
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(all_fields_missing)
    assert exception.value.data == {
        "id": "REQUIRED",
        "date": "REQUIRED",
        "title": "REQUIRED",
        "category": "REQUIRED",
        "status": "REQUIRED",
        "user_id": "REQUIRED",
    }

    id_missing = {
        "date": "2020-02-05",
        "title": "test-title",
        "category": "test-category",
        "status": 1,
        "user_id": "user-1"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(id_missing)
    assert exception.value.data == {
        "id": "REQUIRED",
    }

    date_missing = {
        "id": "test-id",
        "title": "test-title",
        "category": "test-category",
        "status": 1,
        "user_id": "user-1"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(date_missing)
    assert exception.value.data == {
        "date": "REQUIRED",
    }

    title_missing = {
        "id": "test-id",
        "date": "2020-02-05",
        "category": "test-category",
        "status": 1,
        "user_id": "user-1"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(title_missing)
    assert exception.value.data == {
        "title": "REQUIRED",
    }

    category_missing = {
        "id": "test-id",
        "date": "2020-02-05",
        "title": "test-title",
        "status": 1,
        "user_id": "user-1"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(category_missing)
    assert exception.value.data == {
        "category": "REQUIRED",
    }

    status_missing = {
        "id": "test-id",
        "date": "2020-02-05",
        "title": "test-title",
        "category": "test-category",
        "user_id": "user-1"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(status_missing)
    assert exception.value.data == {
        "status": "REQUIRED",
    }

    user_id_missing = {
        "id": "test-id",
        "date": "2020-02-05",
        "title": "test-title",
        "category": "test-category",
        "status": 1
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(user_id_missing)
    assert exception.value.data == {
        "user_id": "REQUIRED",
    }


def test_should_get_BadRequestError_if_the_date_isnt_in_iso8601_format(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    data = {
        "id": "test-id",
        "date": "date-with-wrong-format",
        "title": "test-title",
        "category": "test-category",
        "status": 1,
        "user_id": "user-1"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(data)
    assert exception.value.data == {
        "date": "BAD FORMAT"
    }


def test_should_get_BadRequestError_if_the_goal_status_isnt_zero_or_one(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    data = {
        "id": "test-id",
        "date": "2020-03-15",
        "title": "test-title",
        "category": "test-category",
        "status": "status-with-wrong-format",
        "user_id": "user-1"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_assigned_users_goal(data)
    assert exception.value.data == {
        "status": "BAD VALUE"
    }


def test_should_get_NotFoundError_if_the_user_doesnt_exist(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    data = {
        "id": "test-id",
        "date": "2020-03-21",
        "title": "test-title",
        "category": "test-category",
        "status": 1,
        "user_id": "user-doesnt-exist"
    }
    with pytest.raises(NotFoundError) as exception:
        goal_interactor.save_assigned_users_goal(data)
    assert exception.value.data == {
        "msg": "User with id 'user-doesnt-exist' not found."
    }


def test_should_get_NotFoundError_if_the_user_is_not_assigned_to_the_admin(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    data = {
        "id": "test-id",
        "date": "2020-03-21",
        "title": "test-title",
        "category": "test-category",
        "status": 1,
        "user_id": "user-1"
    }
    with pytest.raises(NotFoundError) as exception:
        goal_interactor.save_assigned_users_goal(data)
    assert exception.value.data == {
        "msg": "User with id 'user-1' not found."
    }


def test_should_get_NotAuthorizedError_if_the_admin_is_not_logged_in(database):
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: None,
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(
        None, goal_repository, user_repository)
    data = {
        "id": "test-id",
        "date": "2020-03-21",
        "title": "test-title",
        "category": "test-category",
        "status": 1,
        "user_id": "user-1"
    }
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.save_assigned_users_goal(data)
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
        None, goal_repository, user_repository)
    data = {
        "id": "test-id",
        "date": "2020-03-21",
        "title": "test-title",
        "category": "test-category",
        "status": 1,
        "user_id": "user-1"
    }
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.save_assigned_users_goal(data)
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
