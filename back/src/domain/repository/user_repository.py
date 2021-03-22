from src.domain.model.user import User
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
