import base.transactions.create as create
import base.transactions.transfer as transfer
import base.user as user
import base.connection as connection
import base.asset as asset
import base.metadata as metadata
import base.transactions.combine as combine

bob = user.User()
alice = user.User()

connection = connection.Connection('http://localhost:9984').get_connection()

asset = asset.Asset(amount=1000)
metadata = metadata.Metadata()

create_transaction = create.Create(connection=connection, user=bob, asset=asset, metadata=metadata)
create_transaction.execute()

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


transfer_transaction3 = transfer.Transfer(
    connection=connection,
    transaction_id=transfer_transaction2.transaction.transaction_id,
    outputs=transfer_transaction2.transaction.outputs,
    recipient=alice,
    owner=bob,
    asset_id=create_transaction.transaction.transaction_id,
    amount=50
)
transfer_transaction3.execute()

combine_transaction = combine.Combine(connection=connection, user=alice).combine()

print(combine_transaction.outputs[0]['amount'])

