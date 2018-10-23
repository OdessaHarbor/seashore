from flask import Flask, Request, abort, jsonify
from flask_restful import Resource, Api, reqparse
import json
import requests


def create_converter():
    app = Flask(__name__)

    parser = reqparse.RequestParser()
    parser.add_argument("amount", type=float, required=True, location="args")
    parser.add_argument("input_currency", required=True, location="args")
    parser.add_argument("output_currency", location="args")

    class Converter(Resource):
        def get(self):
            args = parser.parse_args()
            amount = args["amount"]
            inp_cur = args["input_currency"]
            out_cur = args["output_currency"]
            #get rates from API
            data = {"base":inp_cur}
            try:
                resp = requests.get(app.config["RATES_API"], params=data)
            except Exception:
                abort(500)
            if resp.status_code == 200:
                rates = resp.json()["rates"]
            else:
                abort(resp.status_code, resp.text)
            #convert currency

            if out_cur:
                try:
                    rt = rates[out_cur]
                    conv_amount = (amount * rt)
                    output = {out_cur:conv_amount}
                except KeyError:
                    output = rates
            else:
                for currency in rates:
                    rates[currency] = (amount * rates[currency])
                output = rates

            json_tamplate = {"input":{"amount":amount, "currency":inp_cur}, "output": output}
            return jsonify(json_tamplate)

    api = Api(app)
    api.add_resource(Converter, '/currency_converter')

    app.config.from_pyfile("D:\\Sources\\Converter\\config\\settings.py")
    return app


