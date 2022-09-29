from decimal import Decimal
import re
from types import NoneType
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import BidForm, NewListingForm, CommentForm
from datetime import datetime
from .models import Auction_listing, Bids, Comments, Category
from .models import User

def index(request):
    listings = Auction_listing.objects.all().order_by('-date')

    #list = []

    #for item in listings:
        #if item.status is True:
            #list.append(item)

    pager = Paginator(listings, 6)
    page = request.GET.get('page')
    listing = pager.get_page(page)

    return render(request, "auctions/index.html", {
        "listing": listing,
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
    form1 = CommentForm()
    watched = bool

    if listing.watchlist.filter(id=request.user.id).exists():
        watched = True
    return render(request, "auctions/auction_listing.html", {
        "item": listing,
        "form": form,
        "form1": form1,
        "watched": watched
    })

@login_required(login_url='login')
def watchlist(request, id):

    listing = get_object_or_404(Auction_listing, id=id)

    if listing.watchlist.filter(id=request.user.id).exists():
        listing.watchlist.remove(request.user)
    else:  
        listing.watchlist.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
@login_required(login_url='login')
def watchlist_page(request):
    watched_list = Auction_listing.objects.filter(watchlist=request.user)
    return render(request, "auctions/watchlist.html", {
        "list": watched_list
    })

@login_required(login_url='login')
def bids(request, id):
    listing = get_object_or_404(Auction_listing, id=id)
    error = False
    if request.method == "POST":
        amount = Decimal(request.POST.get('amount'))
        if (amount >= listing.starting_bid and (listing.current_bid is None or amount > listing.current_bid)):
            listing.current_bid = amount
            form = BidForm(request.POST)
            instance = form.save(commit = False)
            instance.listing = listing
            instance.user = request.user
            instance.save()
            listing.save()
            return HttpResponseRedirect("auction_listing", id)
        else:
            error = True
            return render(request, "auctions/auction_listing.html", {
            "error": error
            })
    
def close_listing(request, id):
    listing = get_object_or_404(Auction_listing, id=id)
    if request.user == listing.author:
        listing.status = False
        listing.customer = Bids.objects.filter(listing=listing).last().user
        listing.save()

        if (Bids.objects.filter(listing=listing).last().user) is NoneType:
            return HttpResponseBadRequest("It seems like noone have bided on your listing yet")
    return HttpResponseRedirect("auction_listing", id)

@login_required(login_url='login')
def comments(request, id):
    listing = get_object_or_404(Auction_listing, id=id)
    form = CommentForm(request.POST)
    comment = form.save(commit = False)
    comment.listing = listing
    comment.user = request.user
    comment.save()
    return HttpResponseRedirect("auction_listing", id)

def categories(request):
    cat_list = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "cat_list": cat_list
    })

def category_listing(request, name):
    listings =  Auction_listing.objects.filter(categories=name)
    
    return render(request, "auctions/cat_listing.html", {
    "listing": listings,
    "name": name
        })