from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bill", views.bill, name="bill"),
    path("bill/create", views.createBill, name="createBill"),
    path("cart/set_product_quantity/<int:product_id>/<int:wantedQuantity>", views.setProductQuantity, name="setProductQuantity"),
    path("cart/remove_product/<int:product_id>", views.removeProduct, name="cartRemoveProduct"),
    path("category/<int:category_id>/<str:filtered>", views.category, name="category"),
    path("categories/<int:child_category_id>", views.categories, name="categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("product/<str:id>", views.product, name="product"),
    path("product/add_comment/<str:product_id>", views.addProductComment, name="addComment"),
    path("product/set_product_rating/<int:product_id>/<int:rating>", views.setProductRating, name="setProductRating"),
    path("register", views.register, name="register"),
]