import datetime
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.category_name


class TodoItem(models.Model):
    item = models.CharField(max_length=50)
    item_date = models.DateField(default=datetime.date.today)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.item
