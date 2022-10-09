from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from .models import Cart, CartProduct, Product

# A function that gets the current session key and returns it
def _card_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart


# A fuction that calculates the total of the price for the products in the users cart
def _total(cart_products, cart):
    cart.total = 0
    for cart_product in cart_products:
        cart.total = cart.total + cart_product.sub_total()
    cart.save()


# this function tries to get a cart with a cart ID that matches the current session key if no such cart exists then it creates a new cart with the default values
def _getOrCreateCart(request):
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))

    # if no cart was found then create a cart with the session key as ID and add to it the default vaules
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
                cart_item.save()
            elif product.product_name == "Carrots" or product.product_name == "Onions":
                cart_item = CartProduct.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart,
                )
                cart_item.save()
        cart.save()
    return cart


# the view for the cart.html page
def CartAndProductView(request):
    # gets or creates the user's cart
    cart = _getOrCreateCart(request)

    # get the cart's products and the overall products and then render the page
    cart_products = CartProduct.objects.filter(cart=cart)
    products = Product.objects.all()

    # calulates the price of the products in the inventory
    _total(cart_products, cart)
    context = {"products": products, "carts_products": cart_products, "cart": cart}
    return render(request, "cart.html", context)


# A function that allows the user to buy from the inventory items
def ProductBuy(request, pk):
    cart = _getOrCreateCart(request)
    print(request.POST.get("amount"))
    # checks if the user has entered an amount if not returns an error msg
    if request.POST.get("amount") == "" or request.POST.get("amount") == "0":
        messages.error(
            request,
            f"please enter an amount that is above 0",
        )
    else:

        # if the user has entered an amount then get that amount and get the product that they requested
        amount = float(request.POST.get("amount"))
        product = Product.objects.get(pk=pk)

        # cheskes if the request method is a POST
        if request.method == "POST":
            try:
                cart_product = CartProduct.objects.get(product=product, cart=cart)

                # else if the inventroy amount is bigger then or equal to the amount inputed by the user
                # then add the product to their cart and remove that amount from the inventroy and display a success msg
                if product.quantity >= amount:
                    cart_product.quantity += amount
                    product.quantity -= amount
                    product.save()
                    cart_product.save()
                    messages.success(
                        request,
                        f"{amount} kg of {product.product_name} has been added to your cart",
                    )

                # else if the user input is higher then the inventroy show a error msg
                else:
                    messages.error(
                        request,
                        f"I'm sorry but we only have {product.quantity} of {product.product_name} which isnt enough to fulfill your request of {amount}",
                    )

            # expect that this is the first time the user adds the product to their cart
            except CartProduct.DoesNotExist:

                # if the inventroy amount is bigger then or equal to the amount inputed by the user
                # then create a new entry that stores that product as well as its quantity and the cart its related to.
                # finaly it displays a success msg
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

                # else if the user input is higher then the inventroy show a error msg
                else:
                    messages.error(
                        request,
                        f"I'm sorry but we only have {product.quantity} kg of {product.product_name} which isnt enough to fulfill your request of {amount} kg",
                    )
    cart_products = CartProduct.objects.filter(cart=cart)
    products = Product.objects.all()

    # calulates the price of the products in the inventory
    _total(cart_products, cart)
    context = {"products": products, "carts_products": cart_products, "cart": cart}
    return render(request, "partials/lists.html", context)


# A function that allows the user to remove products from there cart
def ProductDelete(request, pk):

    # checks if the user has entered an amount if not returns an error msg
    if (
        request.POST.get("removeamount") == ""
        or request.POST.get("removeamount") == "0"
    ):
        messages.error(
            request,
            f"please enter an amount that is above 0",
        )
    else:

        # if the user entered an amount that is above 0 then get that amount and
        # the product they wish to reduce or delete and get the product from the inventroy
        amount = float(request.POST.get("removeamount"))
        cart_item = get_object_or_404(CartProduct, pk=pk)
        products = Product.objects.get(product_name=cart_item.product)
        if request.method == "POST":

            # if the user wishes to delete the item then delete it from the cart and add its amount back to the inventory and display a success msg
            if cart_item.quantity == amount:
                products.quantity += amount
                products.save()
                cart_item.delete()
                messages.success(
                    request,
                    f"{cart_item.product} have been removed from your cart",
                )

            # else if the want to reduce the amount they wish to buy the reduce the quantity
            #  of the cart product and add it back to the inventory and display a success msg
            elif cart_item.quantity > amount:
                products.quantity += amount
                cart_item.quantity -= amount
                products.save()
                cart_item.save()
                messages.success(
                    request,
                    f"{amount} kg of {cart_item.product} has been removed from your cart",
                )

            # if the user entered an amount that is bigger then what is currently in there cart then display an error msg
            else:
                messages.error(
                    request,
                    f"couldn't remove {amount} kg from {cart_item.product} because you only hold {cart_item.quantity} kg",
                )
    cart = _getOrCreateCart(request)
    cart_products = CartProduct.objects.filter(cart=cart)
    products = Product.objects.all()
    _total(cart_products, cart)
    context = {"products": products, "carts_products": cart_products, "cart": cart}
    return render(request, "partials/lists.html", context)


# a fuction that allows the user to buy the items inside there cart
def CartBuy(request):

    # get the cart and the product inside there cart
    cart = _getOrCreateCart(request)
    cart_products = CartProduct.objects.filter(cart=cart)

    # if there is not products inside there cart then return an error msg
    if not cart_products:
        messages.error(
            request,
            f"please select a product to buy",
        )

    # else delete the cart product and return a success msg
    else:
        for cart_product in cart_products:
            cart_product.delete()
        cart.total = 0
        cart.save()
        messages.success(
            request,
            f"your cart has been purchased successfully",
        )
    cart_product = CartProduct.objects.filter(cart=cart)
    products = Product.objects.all()
    context = {"products": products, "carts_products": cart_product, "cart": cart}
    return render(request, "partials/lists.html", context)
