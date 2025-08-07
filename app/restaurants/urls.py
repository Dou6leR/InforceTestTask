from django.urls import path
from .views import RestaurantCreateView, RestaurantListView

urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant_list"),
    path("create/", RestaurantCreateView.as_view(), name="restaurant_create"),
]
