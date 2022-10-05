from unittest import mock
from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class meta:
        model = Product
        fields = (
            "product_name",
            "quantity",
            "price",
        )
