import pytest

from rest_framework import status
from django.utils import timezone

from voting.models import Vote


@pytest.mark.django_db
class TestVoteViews:
    def test_create_vote_valid(self, client, user, restaurant, menu_item, get_jwt_token):
        user.restaurant = restaurant
        user.save()
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"menu_item": menu_item.id}
        response = client.post("/api/voting/vote/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Vote.objects.filter(employee=user, menu_item=menu_item).exists()

    def test_create_vote_invalid(self, client, user, restaurant, get_jwt_token):
        user.restaurant = restaurant
        user.save()
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {}  # Missing menu_item
        response = client.post("/api/voting/vote/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_vote_results_old_version(self, client, user, restaurant, menu_item, get_jwt_token):
        user.restaurant = restaurant
        user.save()
        Vote.objects.create(employee=user, menu_item=menu_item, vote_date=timezone.now().date())
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}", HTTP_X_BUILD_VERSION="1.0")
        response = client.get("/api/voting/results/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_vote_results_new_version(self, client, user, restaurant, menu_item, get_jwt_token):
        user.restaurant = restaurant
        user.save()
        Vote.objects.create(employee=user, menu_item=menu_item, vote_date=timezone.now().date())
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}", HTTP_X_BUILD_VERSION="2.0")
        response = client.get("/api/voting/results/")
        assert response.status_code == status.HTTP_200_OK
        assert "vote_count" in response.data[0]

    def test_vote_results_no_restaurant(self, client, user, get_jwt_token):
        token = get_jwt_token(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get("/api/voting/results/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
