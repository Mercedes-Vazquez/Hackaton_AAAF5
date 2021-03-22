from src.domain.repository.goal_repository import GoalRepository
from src.lib.validations import validate_user_authentication
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
        all_tasks = self.goal_repository.get_all_tasks_by_goal_id(
            goal_id)
        return all_tasks
