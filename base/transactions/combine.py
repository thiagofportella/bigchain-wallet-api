import base.transaction as transaction_result

class Combine:
    def __init__(self, connection, user):
        self.connection = connection
        self.user = user

    def combine(self):
        inputs = []
        amount = 0
        asset_id = None

        for output in self.owned_outputs():
            transaction = self.retrieve_transaction(output['transaction_id'])
            output_index = output['output_index']
            inputs.append(self.input_blueprint(transaction['outputs'][output_index],
                                               output_index,
                                               transaction['id']))

            amount += int(transaction['outputs'][output_index]['amount'])

            asset_id = transaction['asset']['id']

        return self.execute_transfer(inputs, asset_id, amount)

    def execute_transfer(self, inputs, asset_id, amount):
        transaction = self.connection.transactions.fulfill(
            self.connection.transactions.prepare(
                operation='TRANSFER',
                asset={'id': asset_id},
                inputs=inputs,
                recipients=[([self.user.public_key], amount)]
            ),
            private_keys=self.user.private_key
        )

        self.connection.transactions.send_commit(transaction)

        combined_transaction = transaction_result.Transaction(
            transaction_id=transaction['id'],
            outputs=transaction['outputs'],
            connection=self.connection,
            owner=self.user,
            asset_id=asset_id
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
