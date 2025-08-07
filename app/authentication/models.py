from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    email = models.EmailField(unique=True)
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", on_delete=models.RESTRICT, null=True,
    )

    class Meta:
        db_table = "employees"

    def __str__(self):
        return self.username
