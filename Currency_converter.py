import sys
import json


RATES_API = "https://api.exchangeratesapi.io/latest"


class Converter():
    """ Converts base currency into target currency """

    def __init__(self, amount, base, target):
        """ 
        param:amount
        param:base
        param:target 
        """
        self.amount = amount
        self.base = base
        self.target = target

    def get_rates(self):
        
