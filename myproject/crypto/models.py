from django.db import models

# crypto/models.py
from django.db import models

class CryptoData(models.Model):
    symbol = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    open_price = models.DecimalField(max_digits=20, decimal_places=8)
    high_price = models.DecimalField(max_digits=20, decimal_places=8)
    low_price = models.DecimalField(max_digits=20, decimal_places=8)
    close_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.symbol} at {self.datetime}"
