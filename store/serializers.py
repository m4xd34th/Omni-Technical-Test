from rest_framework import serializers

from .models import Client, Order, Payment, Product, Shipment


class ClientSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        client = Client.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            full_name=validated_data.get("full_name"),
            address=validated_data.get("address"),
        )
        client.save()
        return client

    class Meta:
        model = Client
        fields = ["full_name", "username", "email", "password", "address"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "quantity", "value"]


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ["address"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["client", "shipment", "cart"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["medium", "order"]
