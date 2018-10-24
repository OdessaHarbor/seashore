from flask import Flask, Request, abort, jsonify
from flask_restful import Resource, Api, reqparse
from flask_caching import Cache
import json
import requests


def create_converter():
    app = Flask(__name__)
    app.config.from_pyfile("D:\\Sources\\Converter\\config\\settings.py")
    app

    parser = reqparse.RequestParser()
    parser.add_argument("amount", type=float, required=True, location="args")
    parser.add_argument("input_currency", required=True, location="args")
    parser.add_argument("output_currency", location="args")

    cache = Cache(app, config={"CACHE_TYPE": "simple"})

    class Converter(Resource):
        """Recives params from Query string and returns json output with converted data """
        def get(self):
            """
            :param amount: amount to convert
            :type amount: float""" 
            self._get_data()
            #get rates from API
            data = {"base":self.inp_cur}
            rates = self._get_rates(data)
            #convert currency
            if self.out_cur:
                try:
                    rt = rates[self.out_cur]
                    conv_amount = (self.amount * rt)
                    output = {self.out_cur:conv_amount}
                except KeyError:
                    output = rates
            else:
                for currency in rates:
                    rates[currency] = (self.amount * rates[currency])
                output = rates

            json_tamplate = {"input":{"amount":self.amount, "currency":self.inp_cur}, "output": output}
            return jsonify(json_tamplate)

        @staticmethod
        @cache.memoize(timeout=300)
        def _get_rates(data):
            try:
                resp = requests.get(app.config["RATES_API"], params=data)
                print("sending request")
            except Exception:
                abort(500)
            if resp.status_code == 200:
                rates = resp.json()["rates"]
            else:
                abort(jsonify(resp.json()))
            return(rates)
        
        
        def _get_data(self):
            """Convert symbols into currency codes """ 
            args = parser.parse_args()
            self.amount = args["amount"]
            self.inp_cur = args["input_currency"]
            self.out_cur = args["output_currency"]

            fl = open(app.config["SYMBOLS_URL"], encoding="utf_8")
            data = json.load(fl)
            for code in data:
                values = data[code]
                if self.inp_cur == values["symbol"]:
                    self.inp_cur = code
                elif self.out_cur == values["symbol"]:
                    self.out_cur = code


    api = Api(app)
    api.add_resource(Converter, '/currency_converter')

    return app


