from django.urls import path

from .views import CartAndProductView, ProductDelete, ProductBuy, CartBuy

urlpatterns = [
    path("", CartAndProductView, name="cart"),
    path("delete/<int:pk>/", ProductDelete, name="ProductDelete"),
    path("buy/<int:pk>/", ProductBuy, name="ProductBuy"),
    path("buycart/", CartBuy, name="CartBuy"),
]
