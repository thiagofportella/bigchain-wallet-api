# Bigchain Crypto-Wallet API

A api-based solution for managing BigchainDB assets in a crypto-wallet context

```python
import base.transactions.create as create
import base.transactions.transfer as transfer
import base.user as user
import base.connection as connection
import base.asset as asset
import base.metadata as metadata
import base.transactions.combine as combine

# Creates two different users, represented by keypairs:
bob = user.User()
alice = user.User()

# Instantiates connection with BigchainDB server:
connection = connection.Connection('http://localhost:9984').get_connection()

# Generate a standard asset with amount set to 1000:
asset = asset.Asset(amount=1000)
metadata = metadata.Metadata()

# Execute a create transaction
create_transaction = create.Create(connection=connection, user=bob, asset=asset, metadata=metadata)
create_transaction.execute()

# Transfer 40 units of the recently created asset to user Alice:
transfer_transaction = transfer.Transfer(
    connection=connection,
    transaction_id=create_transaction.transaction.transaction_id,
    outputs=create_transaction.transaction.outputs,
    recipient=alice,
    owner=bob,
    asset_id=create_transaction.transaction.transaction_id,
    amount=40
)
transfer_transaction.execute()

# Transfer 10 more units to Alice:
transfer_transaction2 = transfer.Transfer(
    connection=connection,
    transaction_id=transfer_transaction.transaction.transaction_id,
    outputs=transfer_transaction.transaction.outputs,
    recipient=alice,
    owner=bob,
    asset_id=create_transaction.transaction.transaction_id,
    amount=10
)
transfer_transaction2.execute()

# Combine those transactions into one, resulting in 50 units to Alice:
combine_transaction = combine.Combine(connection=connection, user=alice).combine()

# Index 0, since there is only one output in the transaction
print(combine_transaction.outputs[0]['amount']) # 50

```
