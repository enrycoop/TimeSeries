from cassandra.cluster import Cluster
from data_access import *
from data_manager import *


def printdata(data):
    for i in range(10):
        print(data[i])


def printSlices(data):
    lengths = [len(slice) for slice in data]
    print(f'min {np.array(lengths).min()}')
    print(f'max {np.array(lengths).max()}')
    print(f'mean {np.array(lengths).mean()}')



if __name__ == '__main__':
    db = DatabaseWrapper()
    data = db.getAllTransactions()
    print('first')
    printdata(data)

    dataManager = DataManager(data=data,indexes=[4,5,6])
    indexed_data = dataManager.nominalToNumeric()
    print('indexed')
    printdata(indexed_data)
    normalized_data = dataManager.normalize(indexes=[2,3])
    print('normalized')
    printdata(normalized_data)
    tm = TimeSeriesConstructor(normalized_data)
    printSlices(tm.construct())
