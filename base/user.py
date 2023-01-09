from bigchaindb_driver.crypto import generate_keypair

class User:
    def __init__(self, public_key = None, private_key = None):
        if public_key is None or private_key is None:
            keypair = generate_keypair()
            self.public_key = keypair.public_key
            self.private_key = keypair.private_key
        else:
            self.public_key = public_key
            self.private_key = private_key

    def public_key(self):
        return self.public_key

    def private_key(self):
        return self.private_key
