from src.lib.sqlite_based_repository import SqliteBasedRepository
from src.domain.model.goal import Goal
from src.domain.model.task import Task


class GoalRepository(SqliteBasedRepository):
    def get_all_goals(self):
        cursor = self._conn().cursor()
        cursor.execute("SELECT * FROM goals;")
        return [
            Goal(id=record["id"], title=record["title"],
                 category=record["category"], status=record["status"],
                 user_id=record["user_id"])
            for record in cursor.fetchall()
        ]

    def get_all_tasks_by_goal_id(self, goal_id):
        cursor = self._conn().cursor()
        cursor.execute("SELECT * FROM tasks WHERE goal_id=?;", (goal_id,))
        return [
            Task(id=record["id"], title=record["title"],
                 description=record["description"], hint=record["hint"],
                 goal_id=record["goal_id"])
            for record in cursor.fetchall()
        ]
        return []
