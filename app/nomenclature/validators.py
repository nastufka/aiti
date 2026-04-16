from rest_framework.exceptions import ValidationError
from .models import Product, Order


def validate_product_exists(product_id: int):
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ValidationError("Товар не найден")


def validate_order_exists(order_id: int):
    try:
        return Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise ValidationError("Заказ не найден")


def validate_product_stock(product, quantity: int):
    if product.quantity < quantity:
        raise ValidationError("Недостаточно товара на складе")