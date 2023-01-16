import datetime

class Metadata:
    def __init__(self, data=None):
        if data is None:
            self.json = self.__default_json()
        else:
            self.json = data

    def __default_json(self):
        return {'datetime': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
