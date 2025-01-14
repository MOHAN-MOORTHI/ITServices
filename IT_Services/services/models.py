

from django.db import models

class Service(models.Model):
    service_name = models.CharField(max_length=200)
    payment_terms = models.CharField(max_length=200)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_package = models.CharField(max_length=200)
    service_tax = models.DecimalField(max_digits=10, decimal_places=2)
    service_image = models.ImageField(upload_to='service_images/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.service_name

class Subscription(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.TextField()
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.service.service_name}"
