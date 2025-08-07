import pytest

from rest_framework import status

from menus.models import Menu


@pytest.mark.django_db
class TestMenuListView:
    def test_menu_list_authenticated(self, client, user, restaurant, menu, get_jwt_token):
        user.restaurant = restaurant
        user.save()
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get("/api/menu/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_menu_list_unauthenticated(self, client):
        response = client.get("/api/menu/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_menu_list_no_restaurant(self, client, user, get_jwt_token):
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get("/api/menu/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_menu_list_admin_all_menus(self, client, admin_user, menu, get_jwt_token):
        token = get_jwt_token(admin_user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get("/api/menu/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestMenuCreateView:
    def test_create_menu_valid(self, client, admin_user, restaurant, get_jwt_token):
        admin_user.restaurant = restaurant
        admin_user.save()
        token = get_jwt_token(admin_user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "restaurant": restaurant.id,
            "menu_items_input": [{"name": "Test Item", "description": "Test Description"}]
        }
        response = client.post("/api/menu/create/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Menu.objects.filter(restaurant=restaurant).exists()

    def test_create_menu_invalid(self, client, admin_user, restaurant, get_jwt_token):
        admin_user.restaurant = restaurant
        admin_user.save()
        token = get_jwt_token(admin_user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "restaurant": restaurant.id,
            # Missing required menu_items_input
        }
        response = client.post("/api/menu/create/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
