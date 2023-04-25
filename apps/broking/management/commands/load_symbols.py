import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.broking.models import Symbol
from nsepy.constants import symbol_list


class Command(BaseCommand):
    help = 'Fetch Nifty50 symbols from API and save to database'

    def handle(self, *args, **options):
        symbols = [
            'ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL',
            'BHARTIARTL', 'INFRATEL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DRREDDY', 'EICHERMOT', 'GAIL',
            'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR', 'HDFC',
            'ICICIBANK', 'ITC', 'IOC', 'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M',
            'MARUTI', 'NTPC', 'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SHREECEM',
            'SBIN', 'SUNPHARMA', 'TCS', 'TATAMOTORS', 'TATASTEEL', 'TECHM', 'TITAN', 'ULTRACEMCO',
            'UPL', 'VEDL', 'WIPRO', 'YESBANK', 'ZEEL',
        ] + list(symbol_list)

        for symbol in symbols:
            url = f'https://dataset.gateway.alphaq.ai/company-{symbol}.json'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                header = data['header']
                details = data['details']

                symbol_obj, created = Symbol.objects.get_or_create(symbol=header['nseScriptCode'])

                symbol_obj.display_name = header.get('displayName', symbol)
                symbol_obj.industry_name = header.get('industryName', symbol)
                symbol_obj.parent_company = details.get('parentCompany', symbol)
                symbol_obj.nse_script_code = header.get('nseScriptCode')
                symbol_obj.is_nse_tradeable = header.get('isNseTradable', False)
                symbol_obj.bse_script_code = header.get('bseScriptCode')
                symbol_obj.is_bse_tradable = header.get('isBseTradable', False)
                symbol_obj.logo_url = header.get('logoUrl')

                symbol_obj.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully saved {symbol_obj}'))

            else:
                self.stderr.write(self.style.ERROR(f'Failed to fetch data for symbol {symbol}. Status code: {response.status_code}'))
