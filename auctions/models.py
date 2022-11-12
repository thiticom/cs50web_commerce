from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name="interestgroups", blank="True")


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
    created_by = models.ForeignKey(
        User,
        null = True,
        related_name="listing_created",
        on_delete = models.SET_NULL
    )
    won_by = models.ForeignKey(
        User,
        null = True,
        related_name="listing_won",
        blank=True,
        on_delete = models.SET_NULL
    )
    closed = models.BooleanField(
        default=False
    )



    def __str__(self):
        return f"{self.title} in {self.cat.all()}"


class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f"bid ${self.bid} in {self.listing} by {self.user}"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f"comment {self.content} in {self.listing} by {self.user}"



