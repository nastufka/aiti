from rest_framework import serializers
from .models import *
from .validators import *


class CategorySerializer(serializers.ModelSerializer):
    ch_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'ch_category']
        depth = 1

    def get_ch_category(self, obj):
        # получение дочерних категорий
        children = obj.children.all()
        if children:
            return CategorySerializer(children, many=True, context=self.context).data
        return []


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category']
        depth = 1


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    order = OrderItemSerializer(read_only=True)


    class Meta:
        model = Order
        fields = ("__all__")
        depth = 1

    def validate(self, attrs):
        product = validate_product_exists(self.initial_data["product_id"])
        order = validate_order_exists(self.initial_data["order_id"])

        validate_product_stock(product, self.initial_data["quantity"])

        attrs["product"] = product
        attrs["order"] = order
        attrs["quantity"] = self.initial_data["quantity"]

        return attrs

    def create(self, validated_data):
        product = validated_data["product"]
        order = validated_data["order"]
        quantity = validated_data["quantity"]

        order_item,_ = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={"quantity": 0}
        )

        order_item.quantity += quantity
        order_item.save()

        product.quantity -= quantity
        product.save()

        return order


class ClientSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Client
        fields = ("__all__")
        depth = 1
