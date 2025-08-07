from django.db import models


class Vote(models.Model):
    employee = models.ForeignKey(
        "authentication.Employee", on_delete=models.CASCADE, null=False
    )
    menu_item = models.ForeignKey(
        "menu_items.MenuItem", on_delete=models.PROTECT, null=False
    )
    vote_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "votes"
        unique_together = ("employee", "vote_date")

    def __str__(self):
        return f"{self.employee.username} voted for {self.menu_item.name} on {self.vote_date}"
