from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator

from . import util
import markdown2, math

from django import forms
from .models import User, Bill, BillDetail, Cart, CartDetail, Category, Comment, DataStorageFeature, DesktopFeature, LaptopFeature, Product, Star

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.TextInput(attrs={'class': 'form-control col-md-10 col-lg-10 formItem', 'placeholder': 'Comment'}))

def addProductComment(request, product_id):
    product = Product.objects.get(id=product_id)

    commentForm = CommentForm(request.POST)
    comment = commentForm['comment'].value()
    Comment(product=product, user=request.user, comment=comment).save()
    
    return HttpResponseRedirect(reverse("product", kwargs={'id': product_id}))

def bill(request):
    cart = Cart.objects.all().filter(user=request.user).first()
    cartDetails = CartDetail.objects.all().filter(cart=cart)
    bills = Bill.objects.all().order_by('-creationDate').values()

    if bills:
        billsExist = 'yes'
    else:
        billsExist = 'no'

    return render(request, "store/bill.html", {
        "cart": cart,
        "cartDetails": cartDetails,
        "bills": bills,
        "billsExist": billsExist
    })

def calculateCategoriesPath(innerCategory):
    parent = innerCategory.parent

    if parent == None:
        categoryList = [innerCategory]
        return categoryList
    else:
        categoryList = calculateCategoriesPath(parent)
        categoryList.append(innerCategory)
        return categoryList

def categories(request, child_category_id):
    category = Category.objects.get(id=child_category_id)
    categoriesPath = calculateCategoriesPath(category)
    childCategories = Category.objects.all().filter(parent=category)

    return render(request, "store/categories.html", {"categoriesPath": categoriesPath, "childCategories": childCategories})

    
    post.postBody = child_category_id['postBody']
    post.save()

    return JsonResponse({"message": "Post updated."}, status=201)

def category(request, category_id, filtered):
    category = Category.objects.get(id=category_id)
    categoriesPath = calculateCategoriesPath(category)

    if (category.id == 3):
        productFilter = "store/product_filter3.html"
    elif (category.id == 5):
        productFilter = "store/product_filter5.html"
    elif (category.id == 6):
        productFilter = "store/product_filter6.html"
    else:
        productFilter = None

    if (filtered != "none"):
        original_products = eval("Product.objects.all().filter(category=category_id," + filtered + ")")
    else:
        original_products = Product.objects.all().filter(category=category_id)

    page = request.GET.get("page", 1)
    paginator = Paginator(original_products, 6)
    products = paginator.page(page)

    return render(request, "store/category.html", {
        "category": category,
        "categoriesPath": categoriesPath,
        "products": products,
        "productFilter": productFilter,
        })

@csrf_exempt
@login_required
def createBill(request):
    cart = Cart.objects.get(user=request.user)
    bill = Bill(user=request.user, totalPrice=cart.totalPrice)
    bill.save()

    cartDetails = CartDetail.objects.all().filter(cart=cart)

    for cartDetail in cartDetails:
        product = Product.objects.get(id=cartDetail.product.id)
        product.stock = product.stock - cartDetail.quantity
        product.save()
        BillDetail(bill=bill, product=cartDetail.product, quantity=cartDetail.quantity, unitPrice=cartDetail.unitPrice, totalPrice=cartDetail.totalPrice).save()

    cartDetails.delete()
    cart.delete()

    return HttpResponseRedirect(reverse("bill"))

def index(request):
    original_products = Product.objects.all().order_by('-id').values()

    page = request.GET.get("page", 1)
    paginator = Paginator(original_products, 6)
    products = paginator.page(page)

    return render(request, "store/index.html", {"products": products})

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
            return render(request, "store/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "store/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def product(request, id):
    product = Product.objects.get(id=id)

    if product != None:
        productDescription = util.get_product(id)
        category = Category.objects.get(id=product.category.id)
        categoriesPath = calculateCategoriesPath(category)
        comments = Comment.objects.all().filter(product=product)

        if (category.id == 3):
            productFeature = DataStorageFeature.objects.all().filter(product=product).values().first()
        elif (category.id == 5):
            productFeature = DesktopFeature.objects.all().filter(product=product).values().first()
        elif (category.id == 6):
            productFeature = LaptopFeature.objects.all().filter(product=product).values().first()
        else:
            productFeature = None

        if productDescription != None:
            productDescription = markdown2.markdown(productDescription)
        else:
            productDescription = "No description."

        if request.user.is_authenticated:
            cart = Cart.objects.all().filter(user=request.user).first()

            if(cart):
                cartDetail = CartDetail.objects.all().filter(cart=cart, product=product).first()
            else:
                cartDetail = None
            
            bought = "False"
            bills = Bill.objects.all().filter(user=request.user)
            
            if(bills):
                for bill in bills:
                    billDetail = BillDetail.objects.all().filter(bill=bill, product=product).first()

                    if billDetail:
                        bought = "True"
                        break
        else:
            bought = "False"
            cartDetail = None

        return render(request, "store/product.html", {
            "bought": bought,
            "cartDetail": cartDetail,
            "categoriesPath": categoriesPath,
            "comments": comments,
            "commentForm": CommentForm(),
            "filter_manager": 'store/product_features' + str(category.id) + ".html",
            "product": product,
            "productFeature": productFeature,
            "productDescription": markdown2.markdown(productDescription)
        })
    else:
        return HttpResponse("Not found")

def productQuantity(product, user): #Delete me
    cart = Cart.objects.all().filter(user=user).first()

    if(cart):
        cartDetail = CartDetail.objects.all().filter(cart=cart, product=product).first()

        if(cartDetail):
            return cartDetail.quantity
        else:
            return 0
    else:
        return 0

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "store/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "store/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "store/register.html")

def removeProduct(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.all().filter(user=request.user).first()

    if(cart):
        cartDetail = CartDetail.objects.get(cart=cart, product=product)

        if(cartDetail):
            cartDetail.delete()
            cart.totalPrice = cart.totalPrice - cartDetail.totalPrice
            cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
@login_required
def setProductQuantity(request, product_id, wantedQuantity):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.all().filter(user=request.user).first()

    if(not cart):
        cart = Cart(user=request.user, totalPrice=0)
        cart.save()

    unitPrice = product.price
    cartDetail = CartDetail.objects.all().filter(cart=cart, product=product).first()

    # Make this calculation as late as possible
    if (wantedQuantity <= product.stock):
        availableQuantity = wantedQuantity
    else:
        availableQuantity = product.stock

    newCartDetailTotalPrice = unitPrice * availableQuantity

    if (cartDetail):
        oldCartDetailTotalPrice = cartDetail.totalPrice
        cartDetail.quantity = availableQuantity
        cartDetail.totalPrice = newCartDetailTotalPrice
        cartDetail.save()
    else:
        oldCartDetailTotalPrice = 0
        cartDetail = CartDetail(cart=cart, product=product, quantity=availableQuantity, unitPrice=unitPrice, totalPrice=newCartDetailTotalPrice)
        cartDetail.save()
    
    cart.totalPrice = cart.totalPrice - oldCartDetailTotalPrice + newCartDetailTotalPrice
    cart.save()

    return JsonResponse({
        "addedItems": availableQuantity,
        "cartDetailTotalPrice": cartDetail.totalPrice,
        "cartTotalPrice": cart.totalPrice
        }, status=201)

@csrf_exempt
@login_required
def setProductRating(request, product_id, rating):
    product = Product.objects.get(id=product_id)
    stars = Star.objects.all().filter(product=product_id, user=request.user).first()

    if stars:
        stars.rating = rating
        stars.save()
    else:
        Star(product=product, user=request.user, rating=rating).save()

    stars = Star.objects.all().filter(product=product_id)
    starsSum = 0

    for i in stars:
        starsSum = starsSum + i.rating

    floatRating = starsSum / len(stars)
    newRating = math.ceil(floatRating)
    product.rating = newRating
    product.save()

    return JsonResponse({
        "message": "Updated",
        "rating": newRating
        }, status=201)