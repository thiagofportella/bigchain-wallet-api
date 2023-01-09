import base.transactions.transfer as transfer_transaction

class Transaction:
    def __init__(self, transaction_id, outputs, connection, owner_private_key):
        self.transaction_id = transaction_id
        self.outputs = outputs
        self.connection = connection
        self.owner_private_key = owner_private_key

    def transfer(self, recipient):
        return transfer_transaction.Transfer(connection=self.connection,
                                             transaction_id=self.transaction_id,
                                             outputs=self.outputs,
                                             recipient=recipient,
                                             owner_private_key=self.owner_private_key).execute
