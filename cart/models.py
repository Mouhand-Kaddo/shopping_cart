from django.db import models

# Create your models here.
class Product(
    models.Model
):  # Model which represents the product object, which has a name, a quantity,and a price
    product_name = models.CharField(max_length=140)
    quantity = models.FloatField()
    price = models.FloatField()

    def __str__(self):  # String for representing the Model object
        return self.product_name
