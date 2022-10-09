from unicodedata import name
from django.db import models

# Model which represents the product object, which has a name, a quantity,and a price
class Product(models.Model):
    product_name = models.CharField(max_length=140)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)

    # String for representing the Model object
    def __str__(self):
        return self.product_name


# Model which represents the Cart object, which has an ID, the data it was created, and the total price of the cart
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    total = models.FloatField(default=0)

    class Meta:
        db_table = "Cart"

    # String for representing the Model object
    def __str__(self):
        return self.cart_id


# Model which represents the Products that are inside a specfic cart, has a foreign key to a cart,
# and a foreign key to a product, also stores the quantity of the product
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    class Meta:
        db_table = "CartProduct"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "cart"], name="unique_product_cart"
            )
        ]

    # returns a number that represents the ammount that must be paid
    def sub_total(
        self,
    ):
        return self.product.price * self.quantity

    # String for representing the Model object
    def __str__(self):
        return self.product.product_name
