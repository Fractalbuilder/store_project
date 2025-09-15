import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from store.services.auth_service import AuthService
from store.exceptions.common import PasswordMismatchError
from store.repositories.user_repository import UserRepository

pytestmark = pytest.mark.django_db

@pytest.fixture
def rf():
    return RequestFactory()

@pytest.fixture
def mock_create_user(mocker):
    def _create_user(username, email, password):
        User = get_user_model()
        return User.objects.create_user(username=username, email=email, password=password)
    return mocker.patch.object(UserRepository, 'create_user', side_effect=_create_user)

@pytest.fixture
def mock_login(mocker):
    return mocker.patch('store.services.auth_service.login')

def add_session_to_request(request):
    middleware = SessionMiddleware(get_response=lambda r: None)
    middleware.process_request(request)
    request.session.save()

def test_register_user_success(rf, mock_create_user, mock_login):
    request = rf.post('/register/')
    add_session_to_request(request)
    user = AuthService.register_user(request, 'testuser', 'test@example.com', 'pass123', 'pass123')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    mock_create_user.assert_called_once_with('testuser', 'test@example.com', 'pass123')
    mock_login.assert_called_once_with(request, user)

def test_register_user_password_mismatch(rf):
    request = rf.post('/register/')
    with pytest.raises(PasswordMismatchError):
        AuthService.register_user(request, 'testuser', 'test@example.com', 'pass123', 'wrongpass')
