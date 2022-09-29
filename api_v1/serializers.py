from rest_framework import serializers

from webapp.models import Product, Order, OrderProduct


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "amount", "price"]


class NameProdSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']


class OrderProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['order', 'product', 'qty']


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["name", "phone", "address", "created_at", "products", "user"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(instance.order_products.all())
        data["products"] = OrderProductsSerializers(instance.order_products.all(), many=True).data
        return data
