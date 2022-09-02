from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
    path("<int:Auction_listing_id>/auction_listing", views.auction_listing, name="auction_listing"),
    path("<int:id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:id>/bids", views.bids, name="bids"),
    path("<int:id>/close_listing", views.close_listing, name="close_listing"),
    path("<int:id>/comments", views.comments, name="comments"),
    
]