from django.db import models
from django.views.decorators.csrf import csrf_exempt
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    total_price = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    price = models.IntegerField()  # o anki fiyat (snapshot)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

