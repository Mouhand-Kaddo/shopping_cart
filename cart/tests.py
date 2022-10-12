from datetime import datetime
from django.test import TestCase
from django.urls import reverse

from .models import Cart, Product, CartProduct, OrdersPerformed, OrdersItem

# Create your tests here.


class CartTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cart = Cart.objects.create(
            cart_id="test id",
            total=100.5,
        )
        cls.product = Product.objects.create(
            product_name="test product",
            quantity=5.5,
            price=5.5,
        )
        cls.cartproduct = CartProduct.objects.create(
            cart=cls.cart,
            product=cls.product,
            quantity=5.5,
        )
        cls.ordersperformed = OrdersPerformed.objects.create(
            cart=cls.cart,
            total=cls.cart.total,
        )
        cls.orderitem = OrdersItem.objects.create(
            order=cls.ordersperformed,
            product=cls.product,
            quantity=5.5,
        )

    def test_cart_model(self):
        self.assertEqual(self.cart.cart_id, "test id")
        self.assertEqual(self.cart.total, 100.5)
        self.assertEqual(str(self.cart), "test id")

    def test_product_model(self):
        self.assertEqual(self.product.product_name, "test product")
        self.assertEqual(self.product.quantity, 5.5)
        self.assertEqual(self.product.price, 5.5)
        self.assertEqual(str(self.product), "test product")

    def test_cartproduct_model(self):
        self.assertEqual(self.cartproduct.cart, self.cart)
        self.assertEqual(self.cartproduct.product, self.product)
        self.assertEqual(self.cartproduct.quantity, 5.5)
        self.assertEqual(str(self.cartproduct), "test product")
        self.assertEqual(
            float(self.cartproduct.sub_total()),
            self.cartproduct.product.price * self.cartproduct.quantity,
        )

    def test_ordersperformed_model(self):
        self.assertEqual(self.ordersperformed.cart, self.cart)
        self.assertEqual(self.ordersperformed.total, self.cart.total)

    def test_orderitem_model(self):
        self.assertEqual(self.orderitem.order, self.ordersperformed)
        self.assertEqual(self.orderitem.product, self.product)
        self.assertEqual(self.orderitem.quantity, 5.5)
        self.assertEqual(
            float(self.orderitem.sub_total()),
            self.orderitem.product.price * self.orderitem.quantity,
        )

    def test_url_exists_at_correct_location_cart(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_cart_view(self):
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart.html")

    def test_url_exists_at_correct_location_cart(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_delete(self):
        response = self.client.get("/delete/1")
        self.assertEqual(response.status_code, 301)

    def test_url_exists_at_correct_location_buy(self):
        response = self.client.get("/buy/1")
        self.assertEqual(response.status_code, 301)

    def test_url_exists_at_correct_location_buycart(self):
        response = self.client.get("/buycart/")
        self.assertEqual(response.status_code, 200)
