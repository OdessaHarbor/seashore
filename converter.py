import sys
import requests
import json
import re
import argparse

RATES_API = "https://api.exchangeratesapi.io/latest"
SUPPORTED_CURRENCIES = ["USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB", 
"TRY", "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"]

class Converter():
    """ Converts base currency into target currency. """

    def __init__(self):
        """param:input  """ 
        self.input = self._get_input()
        self.rates = {}

    def get_rates(self):
        if self.input.input_currency:
            data = {"base":self.input.input_currency}
        try:
            resp = requests.get(RATES_API, params=data)
        except Exception as a:
            sys.exit("Couldn't connect to API: {}".format(a))
        if resp.status_code == 200:
            self.rates = resp.json()["rates"]
        else:
            sys.exit("\nCouldn't get rates from API: {}, {}\n".format(resp.status_code, resp.text))


    def convert(self):
        self.get_rates()
        try:
            tar_rt = self.rates[self.input.output_currency]
            conv_amount = (self.input.amount * tar_rt)
            output = {self.input.output_currency:conv_amount}
        except KeyError:
            print("\nOutput currency is not supported\n")
            output = self.rates

        json_tamplate = {"input":{"amount":self.input.amount, "currency":self.input.input_currency }, "output": output}
        print(json.dumps(json_tamplate, indent=4))
    

    def _get_input(self):
        try:
            fl = open("Common-Currency.json", encoding="utf_8")
            data = json.load(fl)
        except Exception as f:
            sys.exit(f)
        parser = argparse.ArgumentParser(description="Convert currency based on latest rates from European Central Bank")
        parser.add_argument("--amount", type=float, help="Amount to convert")
        parser.add_argument("--input_currency", type=str, metavar="C", help="Currency code or symbol")
        parser.add_argument("--output_currency", type=str, metavar="C", help="Currency code or symbol")
        parser.add_argument("-l", metavar="", action="store_const", const="list", help="Show list of supported currencies")
        input = parser.parse_args()
        for code in data:
            values = data[code]
            if input.input_currency == values["symbol"]:
                input.input_currency = code
            elif input.output_currency == values["symbol"]:
                input.output_currency = code
            else: continue
        if input.l:
            sys.exit(SUPPORTED_CURRENCIES)
        return input


b = Converter()
b.convert()