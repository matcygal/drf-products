from django.db import models
from django.core.validators import MinValueValidator, RegexValidator



# Create your models here.
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class Product(models.Model):
    sku = models.CharField(max_length=16, unique=True,validators=[alphanumeric, ])
    name = models.CharField(max_length=255, null = False)
    qty = models.IntegerField(
        null = False, 
        default=0,
        validators=[
            MinValueValidator(0)
        ])
    price = models.DecimalField(
        null = False,
        max_digits=7, 
        decimal_places=2, 
        default=0.00,
        )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.sku
    class Meta:
        verbose_name_plural = "Products"
