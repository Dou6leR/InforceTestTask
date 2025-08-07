import pytest

from rest_framework import status

from authentication.models import Employee


@pytest.mark.django_db
class TestRegisterView:
    def test_register_employee_as_admin(self, client, admin_user, get_jwt_token, restaurant):
        token = get_jwt_token(admin_user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "username": "newemployee",
            "email": "employee@example.com",
            "password": "test123",
            "restaurant": restaurant.id,
        }
        response = client.post("/api/auth/register/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Employee.objects.filter(username="newemployee").exists()

    def test_register_employee_as_non_admin(self, client, user, get_jwt_token, restaurant):
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "username": "newemployee",
            "email": "employee@example.com",
            "password": "test123",
            "restaurant": restaurant.id,
        }
        response = client.post("/api/auth/register/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
