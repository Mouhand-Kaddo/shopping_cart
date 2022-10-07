from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart, CartProduct, Product


# Create your views here.
def _card_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart


def CartAndProductView(request):
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_card_id(request))

        cart.save()
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
            cart_product.quantity += 1
            cart_product.save()
        except CartProduct.DoesNotExist:
            cart_item = CartProduct.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            cart_item.save()
        return redirect("/")
    return render(request, "cart.html")


def ProductDelete(request, pk):
    product = get_object_or_404(CartProduct, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("/")
    return render(request, "cart.html", {"product": product})
