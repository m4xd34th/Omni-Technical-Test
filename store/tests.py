import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from store.models import Client, Order, Payment, Product, Shipment


class ModelsTest(TestCase):
    client = APIClient()

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        client = Client.objects.create_user(
            username="testuser",
            email="test_user@omni.com",
            password="test123",
            full_name="test user",
            address="Fake St 123",
        )
        client.save()

        product1 = Product.objects.create(name="Airfryer", quantity=10, value=250000)
        product1.save()

        product2 = Product.objects.create(name="Coffee Maker", quantity=5, value=110000)
        product2.save()

        shipment = Shipment.objects.create(
            address="Calle 33 # 8A - 29, Brr Santa Clara"
        )
        shipment.save()

        order = Order.objects.create(
            client=client,
            shipment=shipment,
        )
        order.save()
        order.cart.set([product1.pk, product2.pk])

        payment = Payment.objects.create(medium=Payment.CREDIT_CARD)
        payment.save()
        payment.order.add(order.pk)

    def test_client_is_active(self):
        client = Client.objects.get(id=1)
        self.assertTrue(client.is_active)

    def test_client_is_staff(self):
        client = Client.objects.get(id=1)
        self.assertFalse(client.is_staff)

    def test_client_object_name_is_readable(self):
        client = Client.objects.get(id=1)
        expected_object_name = f"Client {client.username}"
        self.assertEqual(expected_object_name, str(client))

    def test_products_quantity_equals_to_ten(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.quantity, 10)

    def test_products_object_name(self):
        product = Product.objects.get(id=1)
        expected_object_name = f"Product {product.name}"
        self.assertEqual(expected_object_name, str(product))

    def test_shipment_address(self):
        shipment = Shipment.objects.get(id=1)
        self.assertEqual(shipment.address, "Calle 33 # 8A - 29, Brr Santa Clara")

    def test_shipment_object_name(self):
        shipment = Shipment.objects.get(id=1)
        expected_object_name = f"Shipment #{shipment.pk} to {shipment.address}"
        self.assertEqual(expected_object_name, str(shipment))

    def test_order_number_of_orders_created(self):
        orders = Order.objects.all()
        self.assertEqual(orders.count(), 1)

    def test_order_quantity_of_items_in_cart(self):
        order = Order.objects.get(id=1)
        quantity_of_items = order.cart.all().count()
        self.assertEqual(quantity_of_items, 2)

    def test_order_item_in_cart_is_airfryer(self):
        order = Order.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        self.assertEqual(order.cart.get(id=product2.pk), product2)

    def test_order_item_is_instance_of_product(self):
        order = Order.objects.get(id=1)
        self.assertIsInstance(order.cart.get(id=1), Product)

    def test_order_object_name(self):
        order = Order.objects.get(id=1)
        expected_object_name = f"Order #{order.pk} client {order.client.full_name}"
        self.assertEqual(expected_object_name, str(order))

    def test_payment_method_is_credit_card(self):
        payment = Payment.objects.get(id=1)
        self.assertEqual(int(payment.medium), Payment.CREDIT_CARD)

    def test_payment_object_name(self):
        payment = Payment.objects.get(id=1)
        expected_object_name = f"Payment method {payment.medium}"
        self.assertEqual(expected_object_name, str(payment))

    # def test_api_client_creation_without_login(self):
    #     response = self.client.post(
    #         "/api/v1/store/client/",
    #         {
    #             "full_name": "Test Client",
    #             "username": "testing",
    #             "email": "testing@omni.com",
    #             "password": "test123",
    #             "address": "Fake St 123",
    #         },
    #         format="multipart"
    #     )
    #     self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_api_client_creation_with_login(self):
    #     response = self.client.post(
    #         "/api/v1/store/client/",
    #         {
    #             "full_name": "Test Client",
    #             "username": "testing",
    #             "email": "testing@omni.com",
    #             "password": "test123",
    #             "address": "Fake St 123",
    #         },
    #         format="multipart"
    #     )
    #     self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertContains(
    #         json.loads(response.content),
    #         {
    #             "full_name": "Test Client",
    #             "username": "testing",
    #             "email": "testing@omni.com",
    #             "address": "Fake St 123",
    #         }
    #     )