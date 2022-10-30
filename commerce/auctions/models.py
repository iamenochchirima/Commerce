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
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    date = models.DateTimeField(auto_now_add=True)
    image_link = models.URLField(max_length=600, blank=True,)
    categories = models.CharField(max_length=100, null=True, blank=True, default= None)
    watchlist = models.ManyToManyField(User, related_name="watchlist", default=None, blank=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    status = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", default=None)

    def __str__(self):
        return f"{self.title} {self.starting_bid} {self.description} {self.image_link} {self.categories}"

class Bids(models.Model):
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} {self.date} {self.amount}"

class Comments(models.Model):
    listing = models.ForeignKey(Auction_listing, related_name="comments", on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} {self.date} {self.comment}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"