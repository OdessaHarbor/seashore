from flask_restful import Resource, reqparse
from Converter.core.utils import Worker 
from flask_caching import Cache
from flask import abort, jsonify
import requests
import json
import logging


RATES_API = "https://api.exchangeratesapi.io/latest"
# When not using docker, update with Converter.PATH
SYMBOLS_PATH = "Converter/Symbols.json"


cache = Cache(config={"CACHE_TYPE": "simple"})
# getting logger for flask app
logger = logging.getLogger("Converter")


class Converter_api(Resource):
    """Recives params from Query string and returns json output with converted data."""
    def __init__(self):
        """Configuring parser."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("amount", type=float, required=True, location="args")
        self.parser.add_argument("input_currency", required=True, location="args")
        self.parser.add_argument("output_currency", location="args")
    
    def get(self):
        """Returns converted currency."""
        self._get_data()
        logger.info("data recieved {}, {}, {}".format(self.amount, self.inp_cur, self.out_cur))
        #get rates from API
        data = {"base":self.inp_cur}
        rates = self._get_rates(data)
        #convert currency
        json = Worker(rates, self.amount, self.inp_cur, self.out_cur)
        return jsonify(json.convert())

    @staticmethod
    @cache.memoize(timeout=60*20)
    def _get_rates(data):
        """Returns latest rates from API."""
        try:
            resp = requests.get(RATES_API, params=data)
            logger.info("Sending request to API")
        except Exception:
            logger.warning("Couldn't connect to API. {}, {}".format(RATES_API, data))
            abort(500)
        if resp.status_code == 200:
            logger.info("Status code 200 recieved")
            rates = resp.json()["rates"]
        else:
            logger.warning("Satus code {} recieved with data {}".format(resp.status_code, resp.text))
            abort(jsonify(resp.json()))
        return(rates)
    
    
    def _get_data(self):
        """Convert symbols into currency codes.""" 
        args = self.parser.parse_args()
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