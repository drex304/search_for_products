from django.db import models

from products.constants import SOURCE_CHOICES, SOURCE_CSV, \
COMPESSION_CHOICES, COMPRESSION_NONE


class Product(models.Model):
    ext_id = models.CharField(max_length=64)
    name = models.CharField(max_length=128, default='')
    brand = models.CharField(max_length=256, default='')
    retailer = models.CharField(max_length=128, default='', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0')
    in_stock = models.BooleanField(default=False)
    source = models.IntegerField(choices=SOURCE_CHOICES, default=SOURCE_CSV)

    class Meta:
        unique_together = ('ext_id', 'name')

class Source(models.Model):
    url = models.CharField(max_length=256)
    compression = models.IntegerField(choices=COMPESSION_CHOICES, default=COMPRESSION_NONE)
    format = models.IntegerField(choices=SOURCE_CHOICES, default=SOURCE_CSV)

    def __str__(self):
        return '{}'.format(self.url)
