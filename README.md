# Converter API
Simple API for converting currencies in particular amounts

## Usage
Convert 100 USD into CZK.
'''http
GET /currency_converter?amount=100&input_currency=USD&output_currency=CZK
'''
Convert 100 USD into all known currencies
'''http
/currency_converter?amount=100&input_currency=USD
'''
