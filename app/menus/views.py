from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Menu
from .serializers import MenuSerializer


class MenuListView(APIView):
    authentication_classes = [IsAuthenticated]
    serializer_class = MenuSerializer
    def get(self, request):
        user = request.user

        today = timezone.now().date()
        if user.is_superuser and not user.restaurant:
            menus = Menu.objects.filter(menu_date=today).prefetch_related('menuitem_set')

        elif not user.restaurant:
            return Response({"error": "User must be associated with a restaurant"}, status=status.HTTP_403_FORBIDDEN)

        else:
            menus = Menu.objects.filter(restaurant=user.restaurant, menu_date=today).prefetch_related('menuitem_set')

        serializer = self.serializer_class(menus, many=True)
        return Response(serializer.data)


class MenuCreateView(APIView):
    serializer_class = MenuSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
