class Asset:
    def __init__(self, amount = 1, data = None):
        self.amount = amount

        if data is None:
            self.json = self.__default_json()
        else:
            self.json = data

    def __default_json(self):
        return { 'data': { 'asset': { 'coin': { 'amount': self.amount } } } }
