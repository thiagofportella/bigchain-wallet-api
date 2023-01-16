import base.transaction as transaction_result

class Combine:
    def __init__(self, connection, user, asset_id):
        self.connection = connection
        self.user = user
        self.asset_id = asset_id

        self.inputs = []
        self.amount = 0

    def combine(self):
        for output in self.owned_outputs():
            transaction = self.retrieve_transaction(output['transaction_id'])
            if transaction['operation'] == 'CREATE':
                if self.asset_id != transaction['id']:
                    continue
                else:
                    return self.build_transaction_from_source(transaction)

            if self.asset_id != transaction['asset']['id']:
                continue

            output_index = output['output_index']
            self.append_inputs(transaction=transaction, output_index=output_index)
            self.amount += int(transaction['outputs'][output_index]['amount'])

        return self.execute_transfer()

    def append_inputs(self, transaction, output_index):
        self.inputs.append(self.input_blueprint(transaction['outputs'][output_index],
                                               output_index,
                                               transaction['id']))

    def build_transaction_from_source(self, transaction):
        return transaction_result.Transaction(
            transaction_id=transaction['id'],
            outputs=transaction['outputs'],
            connection=self.connection,
            owner_public_key=self.user.public_key,
            asset_id={'id': transaction['id']}
        )

    def execute_transfer(self):
        transaction = self.connection.transactions.fulfill(
            self.connection.transactions.prepare(
                operation='TRANSFER',
                asset={'id': self.asset_id},
                inputs=self.inputs,
                recipients=[([self.user.public_key], self.amount)]
            ),
            private_keys=self.user.private_key
        )

        self.connection.transactions.send_commit(transaction)

        combined_transaction = transaction_result.Transaction(
            transaction_id=transaction['id'],
            outputs=transaction['outputs'],
            connection=self.connection,
            owner_public_key=self.user.public_key,
            asset_id=self.asset_id
        )

        return combined_transaction

    def input_blueprint(self, output, output_index, transaction_id):
        return {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': transaction_id
            },
            'owners_before': output['public_keys']
        }

    def retrieve_transaction(self, transaction_id):
        return self.connection.transactions.retrieve(transaction_id)

    def owned_outputs(self):
        return self.connection.outputs.get(public_key=self.user.public_key, spent=False)
