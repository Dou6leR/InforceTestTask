import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from authentication.models import Employee
from restaurants.models import Restaurant
from menus.models import Menu
from menu_items.models import MenuItem


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return Employee.objects.create_user(username="testuser", password="testpass123")

@pytest.fixture
def admin_user():
    return Employee.objects.create_superuser(username='admin', password='admin', email='admin@example.com')

@pytest.fixture
def get_jwt_token():
    def _get_jwt_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    return _get_jwt_token

@pytest.fixture
def restaurant():
    return Restaurant.objects.create(name="Test Restaurant")

@pytest.fixture
def menu(restaurant):
    return Menu.objects.create(restaurant=restaurant, menu_date=timezone.now().date())

@pytest.fixture
def menu_item(menu):
    return MenuItem.objects.create(menu=menu, name='Test Item', description='Test Description')
