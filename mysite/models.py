from django.db import models


class ClientResponse(models.Model):
    name = models.CharField(max_length=50, null=False)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_savings = models.DecimalField(max_digits=10, decimal_places=2)
    phone_no = models.CharField(max_length=10)
    email = models.EmailField()
