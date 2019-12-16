import numpy as np
from data_access import *
from data_manager import DataManager, TimeSeriesConstructor, timeDiffinDays
import matplotlib.pyplot as plt
from sklearn.preprocessing import *
from pickle import *
from keras import Sequential
from keras.layers import LSTM, Dense
import arff


def printdata(data):
    for i in range(10):
        print(data[i])


def printSlices(X,y):
    for i in range(10):
        print(X[i],'---->',y[i])

def dump_files(path,test_X, test_y, train_X, train_y ):
    with open(path+'resources/test_X.pkl', 'wb') as fl:
        dump(test_X,fl)

    with open(path+'resources/test_y.pkl', 'wb') as fl:
        dump(test_y,fl)

    with open(path+'resources/train_X.pkl', 'wb') as fl:
        dump(train_X,fl)

    with open(path+'resources/train_y.pkl', 'wb') as fl:
        dump(train_y,fl)
    print('dumped')


def load_files(path):
    with open(path+'resources/test_X.pkl','rb') as fl:
        test_X = load(fl)

    with open(path+'resources/test_y.pkl', 'rb') as fl:
        test_y = load(fl)

    with open(path+'resources/train_X.pkl', 'rb') as fl:
        train_X = load(fl)

    with open(path+'resources/train_y.pkl', 'rb') as fl:
        train_y = load(fl)
    return test_X, test_y, train_X, train_y


db = DatabaseWrapper()
data = db.getAllTransactions()

prev_date = data[0][1]
prev_id = data[0][0]

final_data = []
for i in range(len(data)):
    X = data[i].copy()
    if data[i][0]!=prev_id:
        prev_id = data[i][0]
        X[1] = 0
    else:
        X[1] = timeDiffinDays(data[i][1], prev_date)
    prev_date = data[i][1]
    final_data.append(X)

print(final_data[0:10])
arff.dump('resources/trans.arff', final_data, relation='transactions', names=['account_id','days','amount','balance','k_symbol','operation','type'])



'''
if __name__ == '__main__':
    db = DatabaseWrapper(['82.61.15.68'])
    data = db.getAllTransactions()
    print('first')
    printdata(data)

    dataManager = DataManager(data=data,indexes=[4,5,6])
    indexed_data = dataManager.nominalToNumeric()
    print('indexing')
    printdata(indexed_data)
    n_steps = 7
    tm = TimeSeriesConstructor(indexed_data)
    print('construct slices')
    X,y = tm.construct_slices(slice_dim=n_steps)
    printSlices(X, y)

    test_X, test_y, train_X, train_y = tm.cross_validation(X, y)

    n_features = len(train_X[0][0])
    n_steps = len(train_X[0])
    model = Sequential()
    hidden_nodes = 700
    model.add(LSTM(hidden_nodes, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
    model.add(LSTM(hidden_nodes, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mae')
    model.fit(np.array(train_X), np.array(train_y), epochs=15)

    y_predicted = model.predict(np.array(test_X))
    mae = np.array([abs(x[0] - y) for (x, y) in zip(y_predicted, test_y)]).mean()
    print(f'mae: {mae}')
    print(f'min: {np.array(test_y).min()}')
    print(f'max: {np.array(test_y).max()}')

    array = [(x[0], y) for (x, y) in zip(y_predicted, test_y)]
    # array.sort(key=lambda tup: tup[1])
    y_predicted = [x for (x, y) in array]
    test_y = [y for (x, y) in array]

    _ngraphics = 10
    size = int(len(test_y) / _ngraphics)
    for i in range(_ngraphics):
        plt.figure(figsize=(15, 17))
        plt.plot(test_y[i * size:(i + 1) * size], label='real', color='b', markersize=0.01)
        plt.plot(y_predicted[i * size:(i + 1) * size], linestyle='--', label='predicted', color='g', markersize=0.01)
        plt.ylabel('dollars')
        plt.xlabel('example')
        plt.show()
'''




