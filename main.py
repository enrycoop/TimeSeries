from data_access import *
from data_manager import *


def printdata(data):
    for i in range(10):
        print(data[i])


def printSlices(data):
    for i in range(10):
        print(data[i])


if __name__ == '__main__':
    db = DatabaseWrapper()
    data = db.getAllTransactions()
    print('first')
    #printdata(data)

    dataManager = DataManager(data=data,indexes=[4,5,6])
    indexed_data = dataManager.nominalToNumeric()
    print('indexed')
    #printdata(indexed_data)
    normalized_data = dataManager.normalize(indexes=[2,3])
    print('normalized')
    #printdata(normalized_data)
    tm = TimeSeriesConstructor(normalized_data)
    printSlices(tm.construct())
