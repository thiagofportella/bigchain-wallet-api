import base.transaction as transaction_base

class Create:
    def __init__(self, connection, user, asset, metadata = None):
        self.connection = connection
        self.user = user
        self.asset = asset
        self.metadata = metadata

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
                                                        owner=self.user,
                                                        asset_id=transaction['id'])
        return transaction

    def __prepare_transaction(self):
        return self.connection.transactions.prepare(
                operation='CREATE',
                signers=self.user.public_key,
                recipients=[([self.user.public_key], self.asset.amount)],
                asset=self.asset.json,
                metadata=self.metadata.json,
            )
