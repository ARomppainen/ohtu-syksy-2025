from entities.user import User
from repositories.user_repository import user_repository as default_user_repository


class UserInputError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserService:
    MIN_USERNAME_LENGTH = 3
    MIN_PASSWORD_LENGTH = 8

    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    def create_user(self, username, password, password_confirmation):
        self.validate(username, password, password_confirmation)

        user = self._user_repository.create(User(username, password))

        return user

    def validate(self, username: str, password: str, password_confirmation: str):
        if not username or not password:
            raise UserInputError("Username and password are required")

        if len(username) < UserService.MIN_USERNAME_LENGTH:
            raise UserInputError(
                f"Username too short (min {UserService.MIN_USERNAME_LENGTH} characters)"
            )

        if len(password) < UserService.MIN_PASSWORD_LENGTH:
            raise UserInputError(
                f"Password too short (min {UserService.MIN_PASSWORD_LENGTH} characters)"
            )

        if password.isalpha():
            raise UserInputError("Password invalid (it may not contain only letters)")

        if password != password_confirmation:
            raise UserInputError("Password did not match the confirmation value")


user_service = UserService()
