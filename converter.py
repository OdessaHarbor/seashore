import sys
import requests
import json
import re

RATES_API = "https://api.exchangeratesapi.io/latest"

class Converter():
    """ Converts base currency into target currency. """

    def __init__(self, data):
        """param:  """ 
        self.amount, self.base, self.target = data
    

    def get_rates(self):
        data = {"base":self.base}
        resp = requests.get(RATES_API, params=data)
        if resp.status_code == 200:
            return resp.json()["rates"]
        else:
            sys.exit("Couldn't get rates from API: {}".format(resp.text))

    def convert(self):
        rates = self.get_rates()
        target_amount = (self.amount * rates[self.target])
        json_tamplate = {"input":{"amount":self.amount, "currency":self.base }, "output": {self.target:target_amount}}
        
        print(json.dumps(json_tamplate, indent=4))


def input_check():
    if len(sys.argv) in (5, 7):
        print("go")
        for index, value in enumerate(sys.argv):
            if re.search("amount", value):
                try:
                    amount = float(sys.argv[index + 1])
                except ValueError:
                    print("Amount is not a number")
                    return
            elif re.search("input_currency", value):
                base_curr =  sys.argv[index + 1]
            elif re.search("output_currency", value):
                target_curr = sys.argv[index + 1]
        return(amount, base_curr, target_curr) 

    else :
        print("Not enough parameters")
        return

test = Converter(input_check())
test.convert()

