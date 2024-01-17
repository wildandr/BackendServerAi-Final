# crypto/serializers.py
from rest_framework import serializers
from .models import CryptoData

class CryptoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoData
        fields = ['symbol', 'datetime', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']
