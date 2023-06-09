from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Event(models.Model):
    title = models.CharField(max_length=100)
    category = models.OneToOneField(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now_add=True)
