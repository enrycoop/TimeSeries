import numpy as np
from data_access import *
from data_manager import DataManager, TimeSeriesConstructor, timeDiffinDays
import matplotlib.pyplot as plt
from sklearn.preprocessing import *
from pickle import *
from keras import Sequential
from keras.layers import LSTM, Dense
import arff
from random import randint
from random import seed


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


def load_LSTM_files(path,i,n_train):
    with open(path+f'LSTM_DATA/{i}/test{n_train}_X.pkl','rb') as fl:
        test_X = load(fl)

    with open(path+f'LSTM_DATA/{i}/test{n_train}_y.pkl', 'rb') as fl:
        test_y = load(fl)

    with open(path+f'LSTM_DATA/{i}/train{n_train}_X.pkl', 'rb') as fl:
        train_X = load(fl)

    with open(path+f'LSTM_DATA/{i}/train{n_train}_y.pkl', 'rb') as fl:
        train_y = load(fl)
    return test_X, test_y, train_X, train_y


def create_experimental_data(X, y, dim=(250,500,1000,2000,3500,5000)):
    seed()
    for n in range(10):
        for n_train in dim:
            set_indexes = set()
            while len(set_indexes) < n_train:
                set_indexes.add(randint(0, len(X)))
            train_X = []
            train_y = []
            test_X = []
            test_y = []
            for i in range(len(X)):
                if i in set_indexes:
                    train_X.append(X[i])
                    train_y.append(y[i])
                else:
                    test_y.append(y[i])
                    test_X.append(X[i])
            with open(f'LSTM_DATA/{n}/train{n_train}_X.pkl', 'wb') as fl:
                dump(np.array(train_X), fl)
            with open(f'LSTM_DATA/{n}/test{n_train}_X.pkl', 'wb') as fl:
                dump(np.array(train_X), fl)
            with open(f'LSTM_DATA/{n}/train{n_train}_y.pkl', 'wb') as fl:
                dump(np.array(train_y), fl)
            with open(f'LSTM_DATA/{n}/test{n_train}_y.pkl', 'wb') as fl:
                dump(np.array(train_y), fl)


if __name__ == '__main__':
    db = DatabaseWrapper()
    data = db.getAllTransactions()
    printdata(data)
    dataManager = DataManager(data=data,indexes=[4,5,6])
    print('acquired')

    indexed_data = dataManager.nominalToNumeric()
    print('indexed')
    printdata(indexed_data)

    n_steps = 7
    tm = TimeSeriesConstructor(indexed_data)

    print('construct slices')
    X,y = tm.construct_slices(slice_dim=n_steps)

    printSlices(X, y)
    create_experimental_data(X, y)

    for dim in (250,500,1000,2000,3500,5000):
        for volta in range(10):
            test_X, test_y, train_X, train_y = load_LSTM_files('', volta, dim)

            n_features = len(train_X[0][0])
            n_steps = len(train_X[0])
            model = Sequential()
            hidden_nodes = 700
            model.add(LSTM(hidden_nodes, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
            model.add(LSTM(hidden_nodes, activation='relu'))
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mae')
            model.fit(np.array(train_X), np.array(train_y), epochs=100)

            y_predicted = model.predict(np.array(test_X))
            mae = np.array([abs(x[0] - y) for (x, y) in zip(y_predicted, test_y)]).mean()
            print(f'mae: {mae}')
            print(f'min: {np.array(test_y).min()}')
            print(f'max: {np.array(test_y).max()}')
        '''
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
