from django.contrib import admin

from .models import Auction_listing, Bids, Comments, Category

# Register your models here.
admin.site.register(Auction_listing)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Category)