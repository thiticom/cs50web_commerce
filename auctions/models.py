from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    startbid = models.FloatField()
    image = models.URLField()
    cat = models.ManyToManyField(Category, related_name="listings", blank=True)


    def __str__(self):
        return f"{self.title} in {self.cat.all()}"






