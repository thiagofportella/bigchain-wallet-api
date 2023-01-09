import datetime

class Asset:
    BRL_CURRENCY = 'BRL'

    def __init__(self, amount, currency = BRL_CURRENCY):
        self.metadata = None
        self.amount = amount
        self.currency = currency

    def generate(self, metadata = None):
        if metadata is None:
            self.metadata = self.__date_metadata()
        return { 'asset': { 'coin': { 'amount': self.amount, 'currency': self.currency } } }

    def get_metadata(self):
        return self.metadata

    def __date_metadata(self):
        return { 'datetime': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') }
