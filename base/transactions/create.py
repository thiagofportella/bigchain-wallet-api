class Create:
    def __init__(self, connection, user, asset):
        self.connection = connection
        self.user = user
        self.asset = asset

    def execute(self):
        self.connection.transactions.send_commit(self.__fulfill_transaction())

    def __fulfill_transaction(self):
        return self.connection.transactions.fulfill(
            self.__prepare_transaction(),
            private_keys = self.user.private_key
        )['id']

    def __prepare_transaction(self):
        return self.connection.transactions.prepare(
                operation='CREATE',
                signers=self.user.public_key,
                asset=self.asset.json,
                metadata=self.asset.metadata
            )
