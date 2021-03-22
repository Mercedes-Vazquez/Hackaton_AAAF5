from src.lib.errors import NotAuthorizedError


class UserInteractor:
    def __init__(self, config, user_repository):
        self.config = config
        self.user_repository = user_repository

    def auth_user(self, username, password):
        user = self.user_repository.get_by_username(username)

        if user is None or not user.check_password(password):
            raise NotAuthorizedError({"msg": "Bad username or password"})

        return user

    def get_current_user(self):
        return self.user_repository.get_current_user()
