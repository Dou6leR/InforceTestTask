from django.db import models


class Menu(models.Model):
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE)
    menu_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "menus"
        unique_together = (("restaurant", "menu_date"),)

    def __str__(self):
        return f"{self.restaurant.name} - {self.menu_date}"
