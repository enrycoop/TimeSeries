from cassandra.cluster import Cluster


class DatabaseWrapper(object):
    def __init__(self, address=None, port=9042):
        if address is None:
            address = ['127.0.0.1']
        self.address = address
        self.port = port

    def getAllTransactions(self):
        cluster = Cluster(self.address, self.port)
        session = cluster.connect('test_transactions')
        rows = session.execute('SELECT * FROM transactions')
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
