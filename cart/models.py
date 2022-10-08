from unicodedata import name
from django.db import models

# Create your models here.
class Product(
    models.Model
):  # Model which represents the product object, which has a name, a quantity,and a price
    product_name = models.CharField(max_length=140)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):  # String for representing the Model object
        return self.product_name


class Cart(
    models.Model
):  # Model which represents the Cart object, which has an ID and the data it was created
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "Cart"

    def __str__(self):  # String for representing the Model object
        return self.cart_id


class CartProduct(
    models.Model
):  # Model which represents the Products that are inside a specfic cart, has a foreign key to a cart,
    # and a foreign key to a product, also stores the price of the product as well as the quantity
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)

    class Meta:
        db_table = "CartProduct"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "cart"], name="unique_product_cart"
            )
        ]

    def sub_total(
        self,
    ):  # returns a number that represents the ammount that must be paid
        return self.product.price * self.quantity

    def __str__(self):  # String for representing the Model object
        return self.product.product_name
