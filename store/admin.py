from django.contrib import admin
from .models import Bill, BillDetail, Cart, CartDetail, Category, Comment, DataStorageFeature, DesktopFeature, LaptopFeature, Product, Star, User

# Register your models here.
admin.site.register(Bill)
admin.site.register(BillDetail)
admin.site.register(Cart)
admin.site.register(CartDetail)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(DataStorageFeature)
admin.site.register(DesktopFeature)
admin.site.register(LaptopFeature)
admin.site.register(Product)
admin.site.register(Star)
admin.site.register(User)