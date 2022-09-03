from dataclasses import fields
from pyexpat import model
from unicodedata import category
from django import forms
from django.forms import ModelForm

from .models import Auction_listing, Bids, Comments, Category

choices = Category.objects.all().values_list('name', 'name')

category_list = []

for item in choices:
    category_list.append(item)

class NewListingForm(ModelForm):
    class Meta:
        model = Auction_listing
        fields = ("title", "description", "starting_bid", "image_link", "categories")

        widgets = {
            "categories": forms.Select(choices=category_list, attrs={'class': 'form-control'})
        }

class BidForm(ModelForm):
    amount: forms.DecimalField()
    class Meta:
        model = Bids
        fields = ["amount"]

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
