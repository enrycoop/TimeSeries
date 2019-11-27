from keras import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adagrad
import numpy as np
from data_access import *
from data_manager import DataManager, TimeSeriesConstructor
import matplotlib.pyplot as plt
from sklearn.preprocessing import *

def printdata(data):
    for i in range(10):
        print(data[i])


def printSlices(X,y):
    for i in range(10):
        print(X[i],'---->',y[i])


if __name__ == '__main__':
    #'82.61.15.68'
    db = DatabaseWrapper(['192.168.1.139'])
    data = db.getAllTransactions()
    print('first')
    printdata(data)

    dataManager = DataManager(data=data,indexes=[4,5,6])
    indexed_data = dataManager.nominalToNumeric()
    print('indexing')
    printdata(indexed_data)
    n_steps = 4
    tm = TimeSeriesConstructor(indexed_data)
    print('construct slices')
    X,y = tm.construct_slices(slice_dim=n_steps)
    printSlices(X, y)
    print('normalizing')
    n_features=len(X[0][0])
    model = Sequential()
    hidden_nodes = 700
    test_X, test_y, train_X, train_y = tm.cross_validation(X, y)
    model.add(LSTM(hidden_nodes, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
    model.add(LSTM(hidden_nodes, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
    model.add(LSTM(hidden_nodes, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
    model.add(LSTM(hidden_nodes, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mae')
    model.fit(np.array(train_X), np.array(train_y),epochs=10)

    y_predicted = model.predict(np.array(test_X))
    mae = np.array([abs(x[0]-y) for (x,y) in zip(y_predicted,test_y)]).mean()
    print(f'mae: {mae}')
    print(f'min: {np.array(test_y).min()}')
    print(f'max: {np.array(test_y).max()}')

    array = [(x[0],y) for (x,y) in zip(y_predicted,test_y)]
    #array.sort(key=lambda tup: tup[1])
    y_predicted = [x for (x,y) in array]
    test_y = [y for (x,y) in array]

    _ngraphics = 10
    size = int(len(test_y)/_ngraphics)
    for i in range(_ngraphics):
        plt.figure(figsize=(15,17))
        plt.plot(test_y[i*size:(i+1)*size],label='real',color='b',markersize=0.01)
        plt.plot(y_predicted[i*size:(i+1)*size],linestyle='--', label='predicted', color='g', markersize=0.01)
        plt.ylabel('dollars')
        plt.xlabel('example')
        plt.show()



