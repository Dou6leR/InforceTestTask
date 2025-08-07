from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]


class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
