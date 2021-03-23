from src.domain.repository.goal_repository import GoalRepository
from src.domain.model.goal import Goal
from src.domain.model.task import Task
from src.lib.validations import \
    validate_required_fields, validate_required_range_of_values, \
    validate_user_authentication, validate_admin_role, validate_date_format
from src.lib.errors import NotFoundError, NotAuthorizedError
from datetime import datetime


class GoalInteractor:
    def __init__(self, config, goal_repository, user_repository=None, get_current_date=lambda: datetime.today().strftime("%Y-%m-%d")):
        self.config = config
        self.goal_repository = goal_repository
        self.user_repository = user_repository
        self.get_current_date = get_current_date

    def get_current_users_daily_goals(self):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        return [goal for goal in self.goal_repository.get_all_goals_by_user_id(current_user.id)
                if goal.date == self.get_current_date()]

    def get_all_tasks_by_goal_id(self, goal_id):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        self._validate_goal_id(goal_id)
        self._validate_goal_access(goal_id, current_user)
        all_tasks = self.goal_repository.get_all_tasks_by_goal_id(
            goal_id)
        return all_tasks

    def get_goals_by_date_and_assigned_user_id(self, date, user_id):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        validate_date_format(date)
        self._validate_user(user_id)
        self._validate_user_assignment(user_id, current_user.id)
        all_goals = self.goal_repository.get_all_goals_by_user_id(
            user_id)
        result = []
        for goal in all_goals:
            if goal.date == date:
                result.append(goal)
        return result

    def save_goal(self, data):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        validate_required_fields(
            data, ["id", "date", "title", "category", "status", "user_id"])
        validate_date_format(data["date"])
        validate_required_range_of_values(
            {"status": data["status"]}, [0, 1])
        self._validate_user(data["user_id"])
        self._validate_user_assignment(data["user_id"], current_user.id)
        goal = Goal(data["id"], data["date"], data["title"],
                    data["category"], data["status"], data["user_id"])
        self.goal_repository.save_goal(goal)

    def delete_goal_by_id(self, goal_id):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        self._validate_goal_id(goal_id)
        goal = self.goal_repository.get_goal_by_id(goal_id)
        self._validate_user_assignment(goal.user_id, current_user.id)
        self.goal_repository.delete_goal_by_id(goal_id)

    def save_task(self, data):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        validate_admin_role(current_user)
        validate_required_fields(
            data, ["id", "title", "description", "hint", "goal_id"])
        self._validate_goal_id(data["goal_id"])
        self._validate_goal_access(data["goal_id"], current_user)
        task = Task(data["id"], data["title"], data["description"],
                    data["hint"], data["goal_id"])
        self.goal_repository.save_task(task)

    def _validate_goal_id(self, goal_id):
        goal = self.goal_repository.get_goal_by_id(goal_id)
        if goal is None:
            errors = {"msg": f"Goal with id '{goal_id}' not found."}
            raise NotFoundError(errors)

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

    def _validate_goal_access(self, goal_id, user):
        goal = self.goal_repository.get_goal_by_id(goal_id)
        if not user.is_admin:
            if goal.user_id != user.id:
                errors = {"msg": "This operation is not authorized."}
                raise NotAuthorizedError(errors)
        else:
            self._validate_user_assignment(goal.user_id, user.id)
