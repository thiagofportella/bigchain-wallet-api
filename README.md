# Bigchain Crypto-Wallet API

A api-based solution for managing BigchainDB assets in a crypto-wallet context

```python
import base.transactions.create as create
import base.transactions.transfer as transfer
import base.user as user
import base.connection as connection
import base.asset as asset

# Creates two different users, represented by keypairs:
bob = user.User()
alice = user.User()

# Instantiates connection with BigchainDB server:
connection = connection.Connection('http://localhost:9984').get_connection()

# Generate a standard asset:
asset = asset.Asset()
asset.generate()

# Execute a create transaction
create_transaction = create.Create(connection=connection, user=bob, asset=asset)
create_transaction.execute()

# Transfer the recently created transaction to user Alice:
transfer_transaction = transfer.Transfer(
    connection=connection,
    transaction_id=create_transaction.transaction.transaction_id,
    outputs=create_transaction.transaction.outputs,
    recipient=alice,
    owner_private_key=bob.private_key
)
transfer_transaction.execute()


print(transfer_transaction.transaction.transaction_id) 
# 9de86ae228b3fc2bfaebf463466bbe5e7011252474149a80ddb379942e5266bb

```
