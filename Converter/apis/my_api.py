from flask import abort, jsonify
from flask_restful import Resource, reqparse
from flask_caching import Cache
from ..core.utils import Worker 
import requests
import json

RATES_API = "https://api.exchangeratesapi.io/latest"
SYMBOLS_PATH = "..\\instance\\Symbols.json"

cache = Cache(config={"CACHE_TYPE": "simple"})
parser = reqparse.RequestParser()
parser.add_argument("amount", type=float, required=True, location="args")
parser.add_argument("input_currency", required=True, location="args")
parser.add_argument("output_currency", location="args")

class Converter(Resource):
        """Recives params from Query string and returns json output with converted data """
        def get(self):
            """Returns converted currency """
            self._get_data()
            #get rates from API
            data = {"base":self.inp_cur}
            rates = self._get_rates(data)
            #convert currency
            converter = Worker(rates, self.amount, self.inp_cur, self.out_cur)
            return jsonify(converter.convert())

        @staticmethod
        @cache.memoize(timeout=60*20)
        def _get_rates(data):
            """Returns latest rates from API."""
            try:
                resp = requests.get(RATES_API, params=data)
                print("sending request")
            except Exception:
                abort(500)
            if resp.status_code == 200:
                rates = resp.json()["rates"]
            else:
                abort(jsonify(resp.json()))
            return(rates)
        
        
        def _get_data(self):
            """Convert symbols into currency codes.""" 
            args = parser.parse_args()
            self.amount = args["amount"]
            self.inp_cur = args["input_currency"]
            self.out_cur = args["output_currency"]
            if not self.inp_cur:
                abort(jsonify({"error": "Input value can't be omitted"}))

            fl = open(SYMBOLS_PATH, encoding="utf_8")
            data = json.load(fl)
            for code in data:
                values = data[code]
                if self.inp_cur == values["symbol"]:
                    self.inp_cur = code
                elif self.out_cur == values["symbol"]:
                    self.out_cur = code