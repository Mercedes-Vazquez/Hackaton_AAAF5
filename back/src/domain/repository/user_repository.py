from src.domain.model.user import User
from src.domain.model.log import Log
from src.lib.sqlite_based_repository import SqliteBasedRepository


def create_user_from_record(record):
    return User(**record)


class UserRepository(SqliteBasedRepository):
    def __init__(self, config, database=None, get_current_user_id=lambda: None):
        super().__init__(config, database)
        self.get_current_user_id = get_current_user_id

    def get_current_user(self):
        cursor = self._conn().cursor()
        cursor.execute(
            "SELECT * FROM users where id = ?;", (self.get_current_user_id(),)
        )
        data = cursor.fetchone()

        if data is not None:
            return create_user_from_record(data)

    def get_by_username(self, username):
        cursor = self._conn().cursor()
        cursor.execute("SELECT * FROM users where username = ?;", (username,))

        data = cursor.fetchone()

        if data is not None:
            return create_user_from_record(data)

    def get_log_by_user_id(self, user_id):
        cursor = self._conn().cursor()
        cursor.execute("SELECT * FROM logs WHERE user_id = ?;", (user_id,))
        return [Log(timestamp=record["timestamp"],
                    user_id=record["user_id"]) for record in cursor.fetchall()]

    def save_log_entry(self, log_entry):
        cursor = self._conn().cursor()
        cursor.execute("INSERT OR REPLACE INTO logs VALUES (:timestamp, :user_id)", {
            "timestamp": log_entry.timestamp,
            "user_id": log_entry.user_id
        })
        self._conn().commit()
