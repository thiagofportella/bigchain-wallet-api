import base.transaction as transferred_transaction

class Transfer:
    def __init__(self, connection, transaction_id, outputs, recipient_public_key, owner, asset_id, amount):
        self.connection = connection
        self.transaction_id = transaction_id
        self.outputs = outputs
        self.recipient_public_key = recipient_public_key
        self.owner = owner
        self.asset_id = asset_id
        self.amount = amount
        self.original_amount = 0

    def execute(self):
        self.connection.transactions.send_commit(self.__fulfill_transaction())

    def __fulfill_transaction(self):
        transaction = self.connection.transactions.fulfill(
            self.__prepare_transaction(),
            private_keys=self.owner.private_key
        )

        self.transaction = transferred_transaction.Transaction(transaction_id=transaction['id'],
                                                                outputs=transaction['outputs'],
                                                                connection=self.connection,
                                                                owner_public_key=self.recipient_public_key,
                                                                asset_id=self.asset_id)

        return transaction

    def __prepare_transaction(self):
        return self.connection.transactions.prepare(
                    operation='TRANSFER',
                    asset={ 'id': self.asset_id },
                    inputs=self.__transfer_input(),
                    recipients= [([self.recipient_public_key], self.amount),
                                 ([self.owner.public_key], self.original_amount - self.amount)]
                )

    def __transfer_input(self):
        outputs = []
        output_index = 0

        for output in self.outputs:
            if output['public_keys'][0] != self.owner.public_key:
                output_index = output_index + 1
                continue

            outputs.append({
                            'fulfillment': output['condition']['details'],
                            'fulfills': {
                                'output_index': output_index,
                                'transaction_id': self.transaction_id
                            },
                            'owners_before': output['public_keys']
            })
            self.original_amount = int(self.outputs[output_index]['amount'])
            output_index = output_index + 1
        return outputs
