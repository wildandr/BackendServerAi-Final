from django.shortcuts import render

# crypto/views.py
from rest_framework import generics
from .models import CryptoData
from .serializers import CryptoDataSerializer
from datetime import datetime, timedelta

class CryptoDataList(generics.ListAPIView):
    serializer_class = CryptoDataSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned data to the last 24 hours,
        by filtering against a 'datetime' query parameter in the URL.
        """
        queryset = CryptoData.objects.all()
        last_24_hours = datetime.now() - timedelta(days=1)
        queryset = queryset.filter(datetime__gte=last_24_hours).order_by('datetime')
        return queryset
    
class CryptoDataDetail(generics.ListAPIView):
    serializer_class = CryptoDataSerializer

    def get_queryset(self):
        """
        Restricts the returned data to a specific symbol and the last 24 hours.
        """
        symbol = self.kwargs['symbol']
        last_24_hours = datetime.now() - timedelta(days=1)
        return CryptoData.objects.filter(symbol=symbol, datetime__gte=last_24_hours).order_by('datetime')
