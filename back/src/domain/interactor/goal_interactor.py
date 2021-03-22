from src.domain.repository.goal_repository import GoalRepository
from src.lib.validations import validate_user_authentication


class GoalInteractor:
    def __init__(self, config, goal_repository, user_repository=None):
        self.config = config
        self.goal_repository = goal_repository
        self.user_repository = user_repository

    def get_all_goals(self):
        current_user = self.user_repository.get_current_user()
        validate_user_authentication(current_user)
        return [goal for goal in self.goal_repository.get_all_goals()
                if goal.user_id == current_user.id]
