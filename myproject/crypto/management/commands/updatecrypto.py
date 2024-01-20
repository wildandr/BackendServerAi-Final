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
            "EMTK.JK", "ACES.JK", "ADRO.JK", "AKRA.JK", "AMRT.JK", "ANTM.JK",
            "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK", "BBTN.JK",
            "BMRI.JK", "BRPT.JK", "CPIN.JK", "ESSA.JK", "EXCL.JK", "GGRM.JK",
            "HRUM.JK", "ICBP.JK", "INDY.JK", "INKP.JK", "INTP.JK", "ITMG.JK",
            "KLBF.JK", "MAPI.JK", "MDKA.JK", "MEDC.JK", "PTBA.JK", "SCMA.JK",
            "SIDO.JK", "SRTG.JK", "TBIG.JK", "TLKM.JK", "TOWR.JK", "TPIA.JK",
            "UNVR.JK", "BRIS.JK", "BUKA.JK", "GOTO.JK", "SMGR.JK", "UNTR.JK",
            "INCO.JK", "INDF.JK", "PGAS.JK",
            
            "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD",
            "BNB-USD", "XRP-USD", "DOGE-USD",
            "LTC-USD", "MATIC-USD", "LINK-USD", "FLOW-USD",
            "THETA-USD", "API3-USD", "MANA-USD", "MTL-USD",
            "ICP-USD", "ETH-BTC", "MATIC-BTC",
        ]

        # Looping terus menerus
        while True:
            for crypto in cryptos:
                self.update_crypto_data(crypto)
            time.sleep(60)  # Tunggu selama 60 detik sebelum memulai lagi

    def update_crypto_data(self, symbol):
        try:
            # Normalisasi simbol: mengganti titik dengan strip
            normalized_symbol = symbol.replace('.', '-')

            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            # Cek data terakhir di database menggunakan simbol yang dinormalisasi
            last_entry = CryptoData.objects.filter(symbol=normalized_symbol).order_by('-datetime').first()
            if last_entry:
                last_date = last_entry.datetime.replace(tzinfo=None)
                if last_date >= start_date:
                    start_date = last_date + timedelta(minutes=1)

            if start_date < end_date:
                new_data = yf.download(symbol, start=start_date, end=end_date, interval='1m')
                if not new_data.empty:
                    new_data.reset_index(inplace=True)

                    for _, row in new_data.iterrows():
                        CryptoData.objects.create(
                            symbol=normalized_symbol,  # Gunakan simbol yang dinormalisasi
                            datetime=row['Datetime'],
                            open_price=row['Open'],
                            high_price=row['High'],
                            low_price=row['Low'],
                            close_price=row['Close'],
                            volume=row['Volume']
                        )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating data for {symbol}: {e}'))