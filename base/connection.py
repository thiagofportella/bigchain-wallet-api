import bigchaindb_driver


def create_connection(root_url):
    return bigchaindb_driver.BigchainDB(root_url)

class Connection:
    pass