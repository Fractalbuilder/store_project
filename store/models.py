from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, default=None, blank=True, null=True)
    name = models.CharField(max_length=50)
    leaf = models.CharField(max_length=5)

class Product(models.Model):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    img_url = models.CharField(max_length=300, blank=True, default='')
    shortDescription = models.CharField(max_length=55)
    stock = models.IntegerField()
    rating = models.IntegerField(default=1)

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bill_user")
    totalPrice = models.FloatField(default=0)
    creationDate = models.DateTimeField(default=now, editable=False)
    paid_for = models.CharField(max_length=5, default='false')

class BillDetail(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="bill_detail_bill")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bill_detail_product")
    quantity = models.IntegerField()
    unitPrice = models.FloatField()
    totalPrice = models.FloatField()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_user")
    totalPrice = models.FloatField(default=0)

class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_detail_cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_detail_product")
    quantity = models.IntegerField()
    unitPrice = models.FloatField()
    totalPrice = models.FloatField()

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comment_product")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    comment = models.CharField(max_length=300)

class DataStorageFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=80)
    hardwareInterface = models.CharField(max_length=80)
    portable = models.CharField(max_length=5)
    storage = models.IntegerField()

class DesktopFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=80)
    ram = models.IntegerField()
    screenSize = models.FloatField()
    storage = models.IntegerField()

class LaptopFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=80)
    ram = models.IntegerField()
    screenSize = models.FloatField()
    storage = models.IntegerField()
    
class Star(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="star_product")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="star_user")
    rating = models.IntegerField(default=1)