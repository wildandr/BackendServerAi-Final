from django.db import models

# forex/models.py
from django.db import models

class ForexData(models.Model):
    symbol = models.CharField(max_length=20)
    datetime = models.DateTimeField()
    open_price = models.DecimalField(max_digits=15, decimal_places=6)
    high_price = models.DecimalField(max_digits=15, decimal_places=6)
    low_price = models.DecimalField(max_digits=15, decimal_places=6)
    close_price = models.DecimalField(max_digits=15, decimal_places=6)

    def __str__(self):
        return f"{self.symbol} at {self.datetime}"
