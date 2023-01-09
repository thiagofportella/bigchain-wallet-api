import datetime

class Asset:
    def __init__(self, amount = 1):
        self.metadata = None
        self.amount = amount
        self.json = None

    def generate(self, metadata = None):
        if metadata is None:
            self.metadata = self.__date_metadata()
        self.json = { 'data': { 'asset': { 'coin': { 'amount': self.amount } } } }

    def __date_metadata(self):
        return { 'datetime': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') }
