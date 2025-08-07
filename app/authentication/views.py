from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .serializers import EmployeeSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]
