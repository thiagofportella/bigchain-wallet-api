import base.transaction as transferred_transaction

class Transfer:
    OUTPUT_INDEX = 0

    def __init__(self, connection, transaction_id, outputs, recipient, owner_private_key):
        self.connection = connection
        self.transaction_id = transaction_id
        self.outputs = outputs
        self.recipient = recipient
        self.owner_private_key = owner_private_key

    def execute(self):
        self.connection.transactions.send_commit(self.__fulfill_transaction())

    def __fulfill_transaction(self):
        transaction = self.connection.transactions.fulfill(
            self.__prepare_transaction(),
            private_keys=self.owner_private_key
        )

        self.transaction = transferred_transaction.Transaction(transaction_id=transaction['id'],
                                                           outputs=transaction['outputs'],
                                                           connection=self.connection,
                                                           owner_private_key=self.recipient.private_key)

        return transaction

    def __prepare_transaction(self):
        return self.connection.transactions.prepare(
                    operation='TRANSFER',
                    asset={ 'id': self.transaction_id },
                    inputs=self.__transfer_input(),
                    recipients=self.recipient.public_key
                )

    def __transfer_input(self):
        output = self.outputs[self.OUTPUT_INDEX]

        return {
                    'fulfillment': output['condition']['details'],
                    'fulfills': {
                        'output_index': self.OUTPUT_INDEX,
                        'transaction_id': self.transaction_id
                    },
                'owners_before': output['public_keys']
                }
