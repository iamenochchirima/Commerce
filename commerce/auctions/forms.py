from dataclasses import fields
from pyexpat import model
from django import forms
from django.forms import ModelForm

from .models import Auction_listing

class NewListingForm(ModelForm):
    class Meta:
        model = Auction_listing
        fields = ("title", "description", "starting_bid", "image_link", "categories")