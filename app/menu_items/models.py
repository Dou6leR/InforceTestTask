from django.db import models


class MenuItem(models.Model):
    menu = models.ForeignKey("menus.Menu", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "menu_items"

    def __str__(self):
        return self.name
