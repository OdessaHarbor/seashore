from core.utils import Worker
import requests
import json
import argparse
import sys


RATES_API = "https://api.exchangeratesapi.io/latest"
PATH = "Symbols.json"
SUPPORTED_CURRENCIES = ["USD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF", "ISK", "NOK", "HRK", "RUB", 
"TRY", "AUD", "BRL", "CAD", "CNY", "HKD", "IDR", "ILS", "INR", "KRW", "MXN", "MYR", "NZD", "PHP", "SGD", "THB", "ZAR"]


class Converter_CLI():
    """ Converts base currency into target currency."""

    def __init__(self, input):
        """
        :param input: comand-line values
        :type input: Namespace obj from parse_args()
        """ 
        self.amount = input.amount
        self.input_currency = input.input_currency
        self.output_currency = input.output_currency
        self.rates = {}

    def get_rates(self):
        """Returns dict with codes and currency rates from API."""
        data = {"base":self.input_currency}
        try:
            resp = requests.get(RATES_API, params=data)
        except Exception as a:
            sys.exit("Couldn't connect to API: {}".format(a))
        if resp.status_code == 200:
            self.rates = resp.json()["rates"]
        else:
            sys.exit("\nCouldn't get rates from API: {}, {}\n".format(resp.status_code, resp.text))


    def start(self):
        """Printing json result of converting."""
        self.get_rates()
        converter = Worker(self.rates, self.amount, self.input_currency, self.output_currency)
        print(json.dumps(converter.convert(), indent=4))
    

def get_input():
    """Returns NameSpace obj with input values from comand-line."""
    try:
        fl = open(PATH, encoding="utf_8")
        data = json.load(fl)
    except Exception as f:
        sys.exit(f)

    parser = argparse.ArgumentParser(description="Convert currency based on latest reference rates from European Central Bank")
    parser.add_argument("--amount", type=float, help="Amount to convert")
    parser.add_argument("--input_currency", type=str, metavar="C", help="Currency code or symbol")
    parser.add_argument("--output_currency", type=str, metavar="C", help="Currency code or symbol")
    parser.add_argument("-l", metavar="", action="store_const", const="list", help="Show list of supported currencies")
    input = parser.parse_args()
    # if not enough or no arguments passed show help
    if input.l:
        sys.exit(SUPPORTED_CURRENCIES)
    if not input.amount or not input.input_currency:
        parser.parse_args(["-h"])
    for code in data:
        values = data[code]
        if input.input_currency == values["symbol"]:
            input.input_currency = code
        elif input.output_currency == values["symbol"]:
            input.output_currency = code
        else: continue
    return input


converter = Converter_CLI(get_input())
converter.start()