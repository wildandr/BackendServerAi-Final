# Di dalam file: crypto/management/commands/updatecrypto.py

from django.core.management.base import BaseCommand
from crypto.models import CryptoData  # Sesuaikan dengan path yang benar ke model Anda
import yfinance as yf
from datetime import datetime, timedelta
import time

class Command(BaseCommand):
    help = 'Update crypto data'

    def handle(self, *args, **kwargs):
        cryptos = [
            "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD",
            "BNB-USD", "XRP-USD", "DOGE-USD",
            "LTC-USD", "MATIC-USD", "LINK-USD", "FLOW-USD",
            "THETA-USD", "API3-USD", "MANA-USD", "MTL-USD",
            "ICP-USD", "ETH-BTC"
        ]

        # Looping terus menerus
        while True:
            for crypto in cryptos:
                self.update_crypto_data(crypto)
            time.sleep(60)  # Tunggu selama 60 detik sebelum memulai lagi

    def update_crypto_data(self, symbol):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            # Cek data terakhir di database
            last_entry = CryptoData.objects.filter(symbol=symbol).order_by('-datetime').first()
            if last_entry:
                last_date = last_entry.datetime.replace(tzinfo=None)
                # Memastikan kita tidak mengunduh data yang sudah ada
                if last_date >= start_date:
                    start_date = last_date + timedelta(minutes=1)

            # Hanya unduh dan simpan jika ada data baru
            if start_date < end_date:
                new_data = yf.download(symbol, start=start_date, end=end_date, interval='1m')
                if not new_data.empty:
                    new_data.reset_index(inplace=True)

                    for _, row in new_data.iterrows():
                        CryptoData.objects.create(
                            symbol=symbol,
                            datetime=row['Datetime'],
                            open_price=row['Open'],
                            high_price=row['High'],
                            low_price=row['Low'],
                            close_price=row['Close'],
                            volume=row['Volume']
                        )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating data for {symbol}: {e}'))