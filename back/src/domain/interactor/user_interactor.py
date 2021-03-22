from src.lib.errors import NotAuthorizedError, NotFoundError
from src.lib.validations import validate_user_authentication, validate_required_fields, validate_iso8601_timestamp, validate_admin_role
from src.domain.model.log import Log
from src.domain.model.user import User, hash_password


class UserInteractor:
    def __init__(self, config, user_repository, goal_repository=None):
        self.config = config
        self.user_repository = user_repository
        self.goal_repository = goal_repository

    def auth_user(self, username, password):
        user = self.user_repository.get_by_username(username)
        if user is None or not user.check_password(password):
            raise NotAuthorizedError({"msg": "Bad username or password"})
        return user

    def register_user(self, data):
        validate_required_fields(data, ["id", "username", "name", "password"])
        current_user = self.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        new_user = User(data["id"], data["username"],
                        data["name"], hash_password(data["password"]), is_admin=False)
        self.user_repository.save_user(new_user)

    def get_all_assigned_users(self):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        assigned_users = self.user_repository.get_all_assigned_users_by_admin_id(
            current_user.id)
        return assigned_users

    def assign_user(self, data):
        validate_required_fields(data, ["user_id"])
        current_user = self.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        self._validate_user(data["user_id"])
        self.user_repository.assign_user(data["user_id"], current_user.id)

    def unassign_user(self, data):
        validate_required_fields(data, ["user_id"])
        current_user = self.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        self._validate_user(data["user_id"])
        self.user_repository.unassign_user(data["user_id"], current_user.id)

    def get_user_by_id(self, id):
        return self.user_repository.get_by_id(id)

    def get_current_user(self):
        return self.user_repository.get_current_user()

    def get_current_users_log(self):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        log = self.user_repository.get_log_by_user_id(current_user.id)
        return log

    def get_current_users_routine_accomplishments(self):
        log = self.get_current_users_log()
        days_of_use = list(
            set(log_entry.timestamp[0:10] for log_entry in log))
        days_of_use.sort()
        return days_of_use

    def update_current_users_log(self, data):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        validate_required_fields(data, ["timestamp"])
        validate_iso8601_timestamp(data["timestamp"])
        log_entry = Log(timestamp=data["timestamp"], user_id=current_user.id)
        self.user_repository.save_log_entry(log_entry)

    def get_current_users_points(self):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        all_goals = self.goal_repository.get_all_goals_by_user_id(
            current_user.id)
        completed_tasks = 0
        for goal in all_goals:
            if goal.status:
                all_tasks = self.goal_repository.get_all_tasks_by_goal_id(
                    goal.id)
                print(all_tasks)
                completed_tasks += len(all_tasks)
        return completed_tasks

    def update_user_profile(self, id, data):
        validate_required_fields(data, ["username", "name", "password"])
        current_user = self.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        self._validate_user(id)
        user = User(id, data["username"],
                    data["name"], hash_password(data["password"]), is_admin=False)
        self.user_repository.save_user(user)

    def get_progress_by_user_id(self, user_id):
        current_user = self.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        self._validate_user(user_id)
        self._validate_user_assignment(user_id, current_user.id)
        all_goals = self.goal_repository.get_all_goals_by_user_id(user_id)
        progress_by_category = {}
        for goal in all_goals:
            current_value = progress_by_category.get(
                goal.category, (0, 0))
            progress_by_category[goal.category] = (
                current_value[0] + goal.status, current_value[1] + 1)
        return progress_by_category

    def _validate_user(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            errors = {"msg": f"User with id '{user_id}' not found."}
            raise NotFoundError(errors)

    def _validate_user_assignment(self, user_id, admin_id):
        assigned_users = self.user_repository.get_all_assigned_users_by_admin_id(
            admin_id)
        assigned_users_ids = [user.id for user in assigned_users]
        if user_id not in assigned_users_ids:
            errors = {"msg": "This operation is not authorized."}
            raise NotAuthorizedError(errors)
