from django.urls import path
from .views import MenuListView, MenuCreateView

urlpatterns = [
    path("create/", MenuCreateView.as_view(), name="create_menu"),
    path("", MenuListView.as_view(), name="show_menu"),
]
