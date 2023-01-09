import bigchaindb_driver

class Connection:
    def __init__(self, root_url):
        self.root_url = root_url
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = self.__create_connection()

        return self.connection

    def __create_connection(self):
        return bigchaindb_driver.BigchainDB(self.root_url)
