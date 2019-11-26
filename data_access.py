from cassandra.cluster import Cluster


class DatabaseWrapper(object):
    """
    This class manage database access.
    """
    def __init__(self, address=None, port=9042):
        if address is None:
            address = ['127.0.0.1']
        self.address = address
        self.port = port

    def getAllTransactions(self):
        cluster = Cluster(self.address, self.port)
        session = cluster.connect('saltedge')
        rows = session.execute('SELECT * FROM transactions')
        print('data extracted.')
        X = []
        for row in rows:
            X.append([
                row.account_id,
                row.date,
                row.amount,
                row.balance,
                row.k_symbol,
                row.operation,
                row.type])
        return X
