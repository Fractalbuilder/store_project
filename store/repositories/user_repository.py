from django.contrib.auth import get_user_model
from django.db import IntegrityError

class UserRepository:
    @staticmethod
    def create_user(username, email, password):
        User = get_user_model()
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return user
        except IntegrityError:
            raise ValueError("Username already taken.")
