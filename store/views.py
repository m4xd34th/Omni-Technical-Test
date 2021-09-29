from datetime import datetime, timedelta

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from commons.rest_framework.mixins import DestroyModelMixin, ListModelMixin

from .models import Client, Order, Payment, Product, Shipment
from .serializers import (
    ClientSerializer,
    OrderSerializer,
    PaymentSerializer,
    ProductSerializer,
    ShipmentSerializer,
)


class BaseViewset(
    mixins.CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ClientViewset(BaseViewset):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProductViewset(BaseViewset):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShipmentViewset(BaseViewset):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


class OrderViewset(BaseViewset):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PaymentViewset(BaseViewset):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


@method_decorator(csrf_exempt, name="dispatch")
class Login(ObtainAuthToken):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.created = datetime.now()
            token.save()
        return Response(
            {
                "token": {
                    "key": token.key,
                    "type": "bearer",
                    "expires": token.created + timedelta(hours=2),
                },
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                },
            },
            status=HTTP_200_OK,
        )


@method_decorator(csrf_exempt, name="dispatch")
class RefreshToken(APIView):
    def post(self, request, *args, **kwargs):
        _, token = request.META["HTTP_AUTHORIZATION"].split(" ")
        try:
            token_obj = Token.objects.get(key=token)
            user = Client.objects.get(id=token_obj.user_id)
            token_obj.created = datetime.now()
            token_obj.save()
        except Client.DoesNotExist:
            return Response(
                [{"error": True, "message": "User does not logged in"}],
                status=HTTP_403_FORBIDDEN,
            )
        return Response(
            [
                {
                    "token": {
                        "key": token_obj.key,
                        "type": "bearer",
                        "expires": token_obj.created + timedelta(hours=2),
                    },
                    "user": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "role": user.role.name,
                    },
                }
            ],
            status=HTTP_200_OK,
        )


@method_decorator(csrf_exempt, name="dispatch")
class Logout(APIView):
    def get(self, request, *args, **kwargs):
        print(request)
        _, token = request.META["HTTP_AUTHORIZATION"].split(" ")
        print(token)
        try:
            token_obj = Token.objects.get(key=token)
            user = Client.objects.get(id=token_obj.user_id)
            token_obj.delete()
        except Client.DoesNotExist:
            return Response([{"logout": False}], status=HTTP_403_FORBIDDEN)
        return Response([{"logout": True, "user": user.username}], status=HTTP_200_OK)
