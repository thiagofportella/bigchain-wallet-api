import base.transaction as transaction_base

class Create:
    def __init__(self, connection, user, asset):
        self.connection = connection
        self.user = user
        self.asset = asset

    def execute(self):
        self.connection.transactions.send_commit(self.__fulfill_transaction())

    def __fulfill_transaction(self):
        transaction = self.connection.transactions.fulfill(
                        self.__prepare_transaction(),
                        private_keys=self.user.private_key
                    )

        self.transaction = transaction_base.Transaction(transaction_id=transaction['id'],
                                                           outputs=transaction['outputs'],
                                                           connection=self.connection,
                                                           owner_private_key=self.user.private_key)
        return transaction

    def __prepare_transaction(self):
        return self.connection.transactions.prepare(
                operation='CREATE',
                signers=self.user.public_key,
                asset=self.asset.json,
                metadata=self.asset.metadata
            )
