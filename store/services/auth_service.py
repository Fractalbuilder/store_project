from django.contrib.auth import login
from ..exceptions.common import PasswordMismatchError
from ..repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def register_user(request, username, email, password, confirmation):
        if password != confirmation:
            raise PasswordMismatchError("Passwords must match.")

        user = UserRepository.create_user(username, email, password)
        login(request, user)
        return user
