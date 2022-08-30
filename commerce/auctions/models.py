from sre_parse import CATEGORIES
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

class User(AbstractUser):
    pass

class Auction_listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image_link = models.URLField(max_length=500)
    category_choices = [
        ("Fashion", "Fashion"),
        ("Electronics", "Electronicts"),
        ("Property", "Property"),
        ("Toys", "Toys"),
        ("Sports and leisure", "Sports and leisure"),
        ("Home", "Home")
    ]
    categories = models.CharField(max_length=100, null=True, blank=True, choices=category_choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.title} {self.starting_bid} {self.description} {self.image_link}"
