from django.db import models
from core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)
    p_category = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)  # у даем удалять, если где-то используется

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['id', 'p_category']


class Product(TimeStampedModel):  # можно отнаследовать от модели core.BaseModel - будет автоматически писаться история изменения полей
    name = models.CharField(max_length=255)  # можно увеличить при необходимости
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)  # не даем удалить, если где-то используется
    quantity = models.PositiveIntegerField()

class Client(TimeStampedModel):
    name = models.CharField(max_length=255)
    address = models.TextField()  # можно добавить уникальность для поля при необходимиости

    class Meta:
        unique_together = ['name', 'address']  # не даем создавать пользователей с одинаковым именем и адрессом


class Order(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)  # не даем удалить, если где-то используется
    # в рамках задания это не указано, но я бы добавила еще поле автора, которое заполняется автоматически на основе данных из rest запроса


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT) # не даем удалить, если где-то используется
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # не даем удалить, если где-то используется
    quantity = models.PositiveIntegerField()
    # в рамках задания не указано, но желательно сохранять текущую цену продукта
