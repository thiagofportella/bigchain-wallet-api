from flask import Flask, request, jsonify, g

from base.transactions.create import Create
from base.transactions.transfer import Transfer
from base.user import User
from base.connection import Connection
from base.asset import Asset
from base.transactions.combine import Combine

app = Flask(__name__)

@app.before_request
def instantiate_connection():
    if request.path == '/signup':
        return

    root_url = request.headers['Network-Url']
    g.connection = Connection(root_url).get_connection()

@app.before_request
def login_user():
    if request.path == '/signup':
        return

    public_key = request.headers['Public-Key']
    private_key = request.headers['Private-Key']
    g.user = User(public_key=public_key, private_key=private_key)

@app.route('/signup', methods=['POST'])
def signup():
    new_user = User()
    credentials = { 'public_key': new_user.public_key }
    return jsonify(credentials), 201, { 'Private-Key': new_user.private_key }

@app.route('/asset', methods=['POST'])
def create_asset():
    data = request.get_json()
    asset_amount_param = int(data['amount'])

    if 'nft' in data:
        nft_data = data['nft']
        asset = Asset(data=nft_data)
    else:
        asset = Asset(amount=asset_amount_param)

    create_transaction = Create(connection=g.connection, user=g.user, asset=asset)
    if 'metadata' in data:
        create_transaction.metadata = data['metadata']

    create_transaction.execute()

    response_data = { 'asset_id': create_transaction.transaction.transaction_id,
                      'create_transaction_id': create_transaction.transaction.transaction_id,
                      'create_transaction_outputs': create_transaction.transaction.outputs }
    return jsonify(response_data), 201

@app.route('/asset/<string:asset_id>/transfer', methods=['POST'])
def transfer_asset(asset_id):
    data = request.get_json()
    amount_to_transfer = data['amount']
    recipient_public_key = data['recipient_public_key']

    combine_transaction_owner = Combine(connection=g.connection, user=g.user, asset_id=asset_id).combine()
    amount_combined = int(combine_transaction_owner.outputs[0]['amount']) - int(data['amount'])

    print('asset id transfer route', asset_id, flush=True)
    transfer_transaction = Transfer(connection=g.connection,
                                    transaction_id=combine_transaction_owner.transaction_id,
                                    outputs=combine_transaction_owner.outputs,
                                    recipient_public_key=recipient_public_key,
                                    owner=g.user,
                                    asset_id=asset_id,
                                    amount=amount_to_transfer)

    transfer_transaction.execute()

    response_data = {
        'transfer_transaction_id': transfer_transaction.transaction.transaction_id,
        'combine_transaction_id': combine_transaction_owner.transaction_id,
        'total_amount_left': str(amount_combined)
    }

    return jsonify(response_data), 200

@app.route('/asset/<string:asset_id>')
def asset_amount(asset_id):
    combine_transaction = Combine(connection=g.connection, user=g.user, asset_id=asset_id).combine()
    amount = combine_transaction.outputs[0]['amount']

    response_data = { 'asset_id': asset_id, 'amount': amount }
    return jsonify(response_data), 200

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)
