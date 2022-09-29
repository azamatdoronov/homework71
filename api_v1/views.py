from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.serializers import ProductsSerializers, OrderSerializers, OrderProductsSerializers
from webapp.models import Product, Order, OrderProduct


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({'status': 'ok'})


class OrdersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        print(self.request.user)
        pk = kwargs.get('pk')
        if pk:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializers(order)
            return Response(serializer.data)
        else:
            order = Order.objects.all()
            serializer = OrderSerializers(order, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(self.request.user)
        order_product = request.data.pop('order_products')
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            if self.request.user.is_authenticated:
                order.user = self.request.user
        for prod in order_product:
            order_prod = OrderProductsSerializers(data={
                'order': order.pk,
                'product': prod.get('product_id'),
                'qty': prod.get('qty')
            })
            order_prod.is_valid(raise_exception=True)
            order_prod.save()
        return Response(serializer.data, status=200)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializers(data=request.data, instance=order)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk)
        Order.delete(order)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderProductsView(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductsSerializers

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializers(data=request.data, instance=order)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk)
        Order.delete(order)
        return Response(status=status.HTTP_204_NO_CONTENT)
