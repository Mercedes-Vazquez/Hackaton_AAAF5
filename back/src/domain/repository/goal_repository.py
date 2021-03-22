from src.lib.sqlite_based_repository import SqliteBasedRepository
from src.domain.model.goal import Goal
from src.domain.model.task import Task


class GoalRepository(SqliteBasedRepository):
    def get_all_goals_by_user_id(self, user_id):
        cursor = self._conn().cursor()
        cursor.execute("SELECT * FROM goals WHERE user_id=?;", (user_id,))
        return [
            Goal(id=record["id"], date=record["date"], title=record["title"],
                 category=record["category"], status=int(record["status"]),
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

    def get_goal_by_id(self, goal_id):
        cursor = self._conn().cursor()
        cursor.execute("SELECT * FROM goals WHERE id=?;", (goal_id,))
        record = cursor.fetchone()
        if record:
            return Goal(id=record["id"], date=record["date"], title=record["title"],
                        category=record["category"], status=record["status"],
                        user_id=record["user_id"])
        return None

    def save_assigned_users_goal(self, goal):
        cursor = self._conn().cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO goals 
            VALUES (:id, :date, :title, :category, :status, :user_id)
        """, {
            "id": goal.id,
            "date": goal.date,
            "title": goal.title,
            "category": goal.category,
            "status": 1 if goal.status else 0,
            "user_id": goal.user_id,
        })
        self._conn().commit()
