from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "username", "email", "password", "restaurant"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Employee.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            restaurant=validated_data["restaurant"]
        )
        return user
