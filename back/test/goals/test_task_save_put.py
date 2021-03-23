from src.domain.repository.user_repository import UserRepository
from src.domain.repository.goal_repository import GoalRepository
from src.domain.interactor.goal_interactor import GoalInteractor
from src.domain.model.user import hash_password
from src.lib.errors import NotAuthorizedError, BadRequestError, NotFoundError
import pytest


def test_should_create_the_goal_if_the_goal_doesnt_exist_and_all_data_is_OK_and_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-1");
        
        INSERT INTO goals VALUES
        ("test-goal-id-1", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "2020-03-16", "test-title", "test-category", 0, "user-1"),
        ("test-goal-id-5", "2020-03-17", "test-title", "test-category", 1, "user-2");
        """
    )
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)
    data = {
        "id": "test-task-id",
        "title": "test-title",
        "description": "test-description",
        "hint": "test-hint",
        "goal_id": "test-goal-id-1"
    }
    goal_interactor.save_task(data)
    tasks = goal_interactor.get_all_tasks_by_goal_id("test-goal-id-1")
    assert len(tasks) == 1
    assert tasks[0].id == "test-task-id"
    assert tasks[0].title == "test-title"
    assert tasks[0].description == "test-description"
    assert tasks[0].hint == "test-hint"
    assert tasks[0].goal_id == "test-goal-id-1"


def test_should_update_the_goal_if_the_goal_exists_and_all_data_is_OK_and_the_admin_is_logged_in(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-1");
        
        INSERT INTO goals VALUES
        ("test-goal-id-1", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "2020-03-16", "test-title", "test-category", 0, "user-1"),
        ("test-goal-id-5", "2020-03-17", "test-title", "test-category", 1, "user-2");

        INSERT INTO tasks VALUES
        ("test-task-id-1", "test-title", "test-description", "test-hint", "test-goal-id-1"),
        ("test-task-id-2", "test-title", "test-description", "test-hint", "test-goal-id-2");
        """)
    user_repository = UserRepository(
        None,
        database,
        get_current_user_id=lambda: "admin-1",
    )
    goal_repository = GoalRepository(None, database)
    goal_interactor = GoalInteractor(None, goal_repository, user_repository)
    data = {
        "id": "test-task-id-1",
        "title": "test-new-title",
        "description": "test-new-description",
        "hint": "test-new-hint",
        "goal_id": "test-goal-id-1"
    }
    goal_interactor.save_task(data)
    tasks = goal_interactor.get_all_tasks_by_goal_id("test-goal-id-1")
    assert len(tasks) == 1
    assert tasks[0].id == "test-task-id-1"
    assert tasks[0].title == "test-new-title"
    assert tasks[0].description == "test-new-description"
    assert tasks[0].hint == "test-new-hint"
    assert tasks[0].goal_id == "test-goal-id-1"


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
        goal_interactor.save_task(all_fields_missing)
    assert exception.value.data == {
        "id": "REQUIRED",
        "title": "REQUIRED",
        "description": "REQUIRED",
        "hint": "REQUIRED",
        "goal_id": "REQUIRED",
    }

    id_missing = {
        "title": "test-title",
        "description": "test-description",
        "hint": "test-hint",
        "goal_id": "test-goal-id"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_task(id_missing)
    assert exception.value.data == {
        "id": "REQUIRED",
    }

    title_missing = {
        "id": "test-id",
        "description": "test-description",
        "hint": "test-hint",
        "goal_id": "test-goal-id"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_task(title_missing)
    assert exception.value.data == {
        "title": "REQUIRED",
    }

    description_missing = {
        "id": "test-id",
        "title": "test-title",
        "hint": "test-hint",
        "goal_id": "test-goal-id"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_task(description_missing)
    assert exception.value.data == {
        "description": "REQUIRED",
    }

    hint_missing = {
        "id": "test-id",
        "title": "test-title",
        "description": "test-description",
        "goal_id": "test-goal-id"
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_task(hint_missing)
    assert exception.value.data == {
        "hint": "REQUIRED",
    }

    goal_id_missing = {
        "id": "test-id",
        "title": "test-title",
        "description": "test-description",
        "hint": "test-hint",
    }
    with pytest.raises(BadRequestError) as exception:
        goal_interactor.save_task(goal_id_missing)
    assert exception.value.data == {
        "goal_id": "REQUIRED",
    }


def test_should_get_NotFoundError_if_the_goal_doesnt_exist(database):
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
        "title": "test-title",
        "description": "test-description",
        "hint": "test-hint",
        "goal_id": "goal-doesnt-exist"
    }
    with pytest.raises(NotFoundError) as exception:
        goal_interactor.save_task(data)
    assert exception.value.data == {
        "msg": "Goal with id 'goal-doesnt-exist' not found."
    }


def test_should_get_NotAuthorizedError_if_the_goal_is_not_accessible_by_the_admin(database):
    database.executescript(
        """
        INSERT INTO admin_users VALUES
        ("admin-1", "user-2");
        
        INSERT INTO goals VALUES
        ("test-goal-id-1", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-2", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-3", "2020-03-15", "test-title", "test-category", 1, "user-1"),
        ("test-goal-id-4", "2020-03-16", "test-title", "test-category", 0, "user-1"),
        ("test-goal-id-5", "2020-03-17", "test-title", "test-category", 1, "user-2");
        """
    )
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
        "title": "test-title",
        "description": "test-description",
        "hint": "test-hint",
        "goal_id": "test-goal-id-1"
    }
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.save_task(data)
    assert exception.value.data == {
        "msg": "This operation is not authorized."
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
        "title": "test-title",
        "description": "test-description",
        "hint": "test-hint",
        "goal_id": "test-goal-id-1"
    }
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.save_task(data)
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
        "title": "test-title",
        "description": "test-description",
        "hint": "test-hint",
        "goal_id": "test-goal-id-1"
    }
    with pytest.raises(NotAuthorizedError) as exception:
        goal_interactor.save_task(data)
    assert exception.value.data == {
        "msg": "This operation is not authorized."
    }
