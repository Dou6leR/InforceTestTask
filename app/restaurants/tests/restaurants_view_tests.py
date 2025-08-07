import pytest

from rest_framework import status

from restaurants.models import Restaurant


@pytest.mark.django_db
class TestRestaurantViews:
    def test_create_restaurant_as_admin(
            self, client, admin_user, get_jwt_token
    ):
        token = get_jwt_token(admin_user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"name": "New Restaurant"}
        response = client.post("/api/restaurants/create/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Restaurant.objects.filter(name="New Restaurant").exists()

    def test_create_restaurant_as_non_admin(self, client, user, get_jwt_token):
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"name": "New Restaurant"}
        response = client.post('/api/restaurants/create/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_restaurants(self, client, user, restaurant, get_jwt_token):
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get("/api/restaurants/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
