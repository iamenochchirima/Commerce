from decimal import Decimal
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import BidForm, NewListingForm
from datetime import datetime
from .models import Auction_listing
from .models import User

def index(request):
    listings = Auction_listing.objects.all().order_by('date')
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    submitted = False
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect("/create_listing?submitted=True")
    
    else:
        form = NewListingForm()
        if "submitted" in request.GET:
            submitted = True
    return render(request, "auctions/create_listing.html", {
        "form": form,
        "submitted": submitted,
    })

def auction_listing(request, Auction_listing_id):
    listing = Auction_listing.objects.get(id=Auction_listing_id)
    form = BidForm()
    return render(request, "auctions/auction_listing.html", {
        "item": listing,
        "form": form
    })

@login_required
def watchlist(request, id):
    listing = get_object_or_404(Auction_listing, id=id)
    if listing.watchlist.filter(id=request.user.id).exists():
        listing.watchlist.remove(request.user)
    else:
        listing.watchlist.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    

@login_required
def watchlist_page(request):
    watched_list = Auction_listing.objects.filter(watchlist=request.user)
    return render(request, "auctions/watchlist.html", {
        "list": watched_list
    })

@login_required
def bids(request, id):
    listing = get_object_or_404(Auction_listing, id=id)
    if request.method == "POST":
        amount = Decimal(request.POST.get('amount'))

        if (amount >= listing.starting_bid and (listing.current_bid is None or amount > listing.current_bid)):
            listing.starting_bid = amount
            form = BidForm(request.POST)
            instance = form.save(commit = False)
            instance.listing = listing
            instance.author = request.user
            listing.save()
    return HttpResponseRedirect("auction_listing", id)

    