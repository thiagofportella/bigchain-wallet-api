import base.transactions.transfer as transfer_transaction

class Transaction:
    def __init__(self, transaction_id, outputs, connection, owner, asset_id):
        self.transaction_id = transaction_id
        self.outputs = outputs
        self.connection = connection
        self.owner = owner
        self.asset_id = asset_id

    def transfer(self, recipient, amount):
        return transfer_transaction.Transfer(connection=self.connection,
                                             transaction_id=self.transaction_id,
                                             outputs=self.outputs,
                                             recipient=recipient,
                                             owner=self.owner,
                                             asset_id=self.asset_id,
                                             amount=amount).execute
