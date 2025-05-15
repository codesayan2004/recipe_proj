from django.contrib import admin
from .models import FoodItem, Wishlist, AdditionalUserInfo
# Register your models here.

admin.site.register(FoodItem)
admin.site.register(Wishlist)
admin.site.register(AdditionalUserInfo)