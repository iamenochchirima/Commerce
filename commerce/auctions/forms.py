from dataclasses import fields
from distutils.command.clean import clean
from email.policy import default
from unicodedata import category
from django import forms
from django.forms import ModelForm

from .models import Auction_listing, Bids, Comments, Category

choices = Category.objects.all().values_list('name', 'name')

category_list = []

for item in choices:
    category_list.append(item)

class NewListingForm(ModelForm):
    categories = forms.ChoiceField( widget= forms.Select(attrs={'class': 'form-control col-md-5 col-lg-6'}), choices=category_list)

    class Meta:
        model = Auction_listing
        fields = ("title", "description", "starting_bid", "image_link", "categories")

        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control col-md-5 col-lg-6'}),
            "description": forms.Textarea(attrs={'class': 'form-control col-md-5 col-lg-6'}),
            "starting_bid": forms.NumberInput(attrs={'class': 'form-control col-md-5 col-lg-6'}),
            "image_link": forms.URLInput(attrs={'class': 'form-control col-md-5 col-lg-6'}),
           
        }

class BidForm(ModelForm):
    amount: forms.DecimalField()
    class Meta:
        model = Bids
        fields = ["amount"]

        widgets = {
            "amount": forms.NumberInput(attrs={'class': 'form-control col-md-5 col-lg-6'})
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]

        widgets = {
            "comment": forms.Textarea(attrs={'class': 'form-control col-md-3 col-lg-6'})
        }
