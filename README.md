# Converter API
Simple API for converting currencies in particular amounts based on latest rates published by [European Central Bank.](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)

### Key features
- Gets rates through [Foreign exchange rates API](https://exchangeratesapi.io/)
- The reference rates are usually updated around 16:00 CET on every working day, except on TARGET closing days.  
- Support symbols as currency values
- Recieved rates are cached for 20 minutes
- Available currencies are limited

## Usage
Convert 100 USD into CZK.
```http
GET /currency_converter?amount=100&input_currency=USD&output_currency=Kč
```

Convert 100 CAD into all known currencies
```http
GET /currency_converter?amount=100&input_currency=CA$
```
Convert 0.9 yen into yuan .
```
GET /currency_converter?amount=0.9&input_currency=¥&output_currency=CN¥
```


## Deployment

Deploy with docker.
```sh
cd seashore
docker-compose up --build
```
