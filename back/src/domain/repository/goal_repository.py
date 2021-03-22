from src.lib.sqlite_based_repository import SqliteBasedRepository
from src.domain.model.goal import Goal


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
