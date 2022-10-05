from django.views.generic import ListView

from .models import Product
# Create your views here.
class ProductListView(ListView): # used a Listview to create a view of all the products
    model = Product
    template_name = "cart.html"