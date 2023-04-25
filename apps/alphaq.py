from typing import List

import requests
import json

headers = {'Content-Type': 'application/json', 'User-Agent': 'PaperTrade / (AlphaQBroker v1.0.0)'}


class AlphaQ:

    LTP_ENDPOINT = "https://api.alphaq.ai/calcs/getLtp"

    def ltp(self, symbols: List[str], exchange: str = 'NSE'):
        payload = json.dumps({
            "ticker": [
                f"{exchange}:{symbol}"
                for symbol in symbols
            ]
        })
        response = requests.request("POST", self.LTP_ENDPOINT, headers=headers, data=payload).json()
        if response['status'] == 'success':
            return {k.split(':')[1]: v['last_price'] for k, v in response['data']['data'].items()}
        return None


