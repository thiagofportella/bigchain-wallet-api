import base.transactions.transfer as transfer_transaction

class Transaction:
    def __init__(self, transaction_id, outputs, connection, owner_public_key, asset_id):
        self.transaction_id = transaction_id
        self.outputs = outputs
        self.connection = connection
        self.owner_public_key = owner_public_key
        self.asset_id = asset_id
