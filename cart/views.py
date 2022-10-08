from django.contrib import messages
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
    # tries to get a cart with a cart ID that matches the current session key
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))

    # if no cart was found then create a cart with the session key as ID
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_card_id(request))
        products = Product.objects.all()
        for product in products:
            if product.product_name == "Potatoes":
                cart_item = CartProduct.objects.create(
                    product=product,
                    quantity=2,
                    cart=cart,
                )
                product.quantity -= 2
                product.save()
                cart_item.save()
            elif product.product_name == "Carrots" or product.product_name == "Onions":
                cart_item = CartProduct.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart,
                )
                product.quantity -= 1
                product.save()
                cart_item.save()
        cart.save()

    # get the carts products and the overall products and then render the page
    cart_product = CartProduct.objects.filter(cart=cart)
    products = Product.objects.all()
    context = {
        "products": products,
        "carts": cart_product,
    }
    return render(request, "cart.html", context)


def ProductBuy(request, pk):
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_card_id(request))
        cart.save()
    if request.POST.get("amount") == "":
        messages.error(
            request,
            f"please enter an amount",
        )
    else:
        amount = float(request.POST.get("amount"))
        product = Product.objects.get(pk=pk)
        if request.method == "POST":
            try:
                cart_product = CartProduct.objects.get(product=product, cart=cart)
                if amount == 0:
                    messages.error(
                        request,
                        f"please enter an amount that is above 0",
                    )
                elif product.quantity >= amount:
                    cart_product.quantity += amount
                    product.quantity -= amount
                    product.save()
                    cart_product.save()
                    messages.success(
                        request,
                        f"{amount} kg of {product.product_name} has been added to your cart",
                    )
                else:
                    messages.error(
                        request,
                        f"I'm sorry but we are out of stock for {product.product_name}",
                    )
            except CartProduct.DoesNotExist:
                if product.quantity >= amount:
                    cart_item = CartProduct.objects.create(
                        product=product,
                        quantity=amount,
                        cart=cart,
                    )
                    product.quantity -= amount
                    product.save()
                    cart_item.save()
                    messages.success(
                        request,
                        f"{amount} kg of {product.product_name} has been added to your cart",
                    )
                else:
                    messages.error(
                        request,
                        f"I'm sorry but we are out of stock for {product.product_name}",
                    )
    cart_product = CartProduct.objects.filter(cart=cart)
    products = Product.objects.all()
    context = {
        "products": products,
        "carts": cart_product,
    }
    return render(request, "partials/lists.html", context)


def ProductDelete(request, pk):
    if request.POST.get("removeamount") == "":
        messages.error(
            request,
            f"please enter an amount",
        )
    else:
        amount = float(request.POST.get("removeamount"))
        cart_item = get_object_or_404(CartProduct, pk=pk)
        Catalog = Product.objects.get(product_name=cart_item.product)
        if request.method == "POST":
            if amount == 0:
                messages.error(
                    request,
                    f"please enter an amount that is above 0",
                )
            elif cart_item.quantity == amount:
                Catalog.quantity += amount
                Catalog.save()
                cart_item.delete()
                messages.success(
                    request,
                    f"{cart_item.product} have been removed from your cart",
                )
            elif cart_item.quantity > amount:
                Catalog.quantity += amount
                cart_item.quantity -= amount
                Catalog.save()
                cart_item.save()
                messages.success(
                    request,
                    f"{amount} kg of {cart_item.product} has been removed from your cart",
                )
            else:
                messages.error(
                    request,
                    f"couldn't remove {amount} kg from {cart_item.product} because you only hold {cart_item.quantity} kg",
                )
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
    return render(request, "partials/lists.html", context)
