

class Worker():
    """Convert base currency into target currency """ 
    def __init__(self, rates, amount, base, target=None):
        self.rates, self.amount, self.base, self.target = rates, amount, base, target

    def convert(self):
        if self.target:
            try:
                rt = self.rates[self.target]
                conv_amount = (self.amount * rt)
                output = {self.target:conv_amount}
            except KeyError:
                output = self._helper()
        else:
            output = self._helper()

        json = {"input":{"amount":self.amount, "currency":self.base}, "output": output}
        return json

    def _helper(self):
        for currency in self.rates:
            self.rates[currency] = (self.amount * self.rates[currency])
        return self.rates