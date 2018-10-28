import logging

logger = logging.getLogger("Converter")

class Worker():
    """Convert base currency into target currency.""" 
    def __init__(self, rates, amount, base, target=None):
        """
        :param rates: recieved rates from api
        :type rates: dict
        :param amount: amount to convert
        :type amount: float
        :param base: input currency to convert
        :type base: str
        :param target: output currency to convert
        :type target: str (optional)
        """
        self.rates, self.amount, self.base, self.target = rates, amount, base, target

    def convert(self):
        """Returns formated dict with data.""" 
        if self.target:
            try:
                rt = self.rates[self.target]
                conv_amount = float("{:.2f}".format((self.amount * rt)))
                output = {self.target:conv_amount}
                logger.info("Converting currency with rate {}".format(rt))
            except KeyError:
                logger.info("Output currency {} is not supported".format(self.target))
                output = self._helper()
        else:
            output = self._helper()

        json = {"input":{"amount":self.amount, "currency":self.base}, "output": output}
        return json

    def _helper(self):
        """Converts into all recieved currencies."""
        logger.info("Converting to all known currencies")
        for currency in self.rates:
            self.rates[currency] = float("{:.2f}".format((self.amount * self.rates[currency])))
        return self.rates