from src.lib.errors import NotAuthorizedError
from src.lib.validations import validate_user_authentication, validate_required_fields, validate_iso8601_timestamp
from src.domain.model.log import Log


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
