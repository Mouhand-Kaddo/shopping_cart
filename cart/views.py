from gettext import Catalog
from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart, CartProduct, Product


# Create your views here.
def _card_id(request):  # A function that gets the current session key and returns it
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart


def CartAndProductView(
    request,
):  # A fucntion that creates the view for the cart.html page
    try:  # tries to get a cart with a cart ID that matches the current session key
        cart = Cart.objects.get(cart_id=_card_id(request))
    except Cart.DoesNotExist:  # if no cart was found then create a cart with the session key as ID
        cart = Cart.objects.create(cart_id=_card_id(request))

        cart.save()
    # get the carts products and the overall products
    cart_product = CartProduct.objects.filter(cart=cart)
    products = Product.objects.all()
    context = {
        "products": products,
        "carts": cart_product,
    }
    return render(request, "cart.html", context)


def ProductBuy(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
        try:
            cart = Cart.objects.get(cart_id=_card_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_card_id(request))

        cart.save()
        try:
            cart_product = CartProduct.objects.get(product=product, cart=cart)
            if product.quantity != 0:
                cart_product.quantity += 1
                product.quantity -= 1
                product.save()
                cart_product.save()
        except CartProduct.DoesNotExist:
            cart_item = CartProduct.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            product.quantity -= 1
            product.save()
            cart_item.save()
        return redirect("/")
    return render(request, "cart.html")


def ProductDelete(request, pk):
    cart_item = get_object_or_404(CartProduct, pk=pk)
    Catalog = Product.objects.get(product_name=cart_item.product)
    if request.method == "POST":
        if cart_item.quantity == 1:
            Catalog.quantity += 1
            Catalog.save()
            cart_item.delete()
        else:
            Catalog.quantity += 1
            cart_item.quantity -= 1
            Catalog.save()
            cart_item.save()
        return redirect("/")
    return render(request, "cart.html", {"product": cart_item})
