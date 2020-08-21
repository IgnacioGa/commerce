from django.contrib import admin

from .models import User, Listing, Bid, Category, Watchlist, Comments, Characteristic

# Register your models here.


admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Characteristic)