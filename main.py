from keras import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adagrad
import numpy as np
from data_access import *
from data_manager import DataManager, TimeSeriesConstructor

from sklearn.preprocessing import *

def printdata(data):
    for i in range(10):
        print(data[i])


def printSlices(X,y):
    for i in range(10):
        print(X[i],'---->',y[i])


if __name__ == '__main__':
    #127.0.0.1 -
    db = DatabaseWrapper()
    data = db.getAllTransactions()
    print('first')
    printdata(data)

    dataManager = DataManager(data=data,indexes=[4,5,6])
    indexed_data = dataManager.nominalToNumeric()
    print('indexing')
    printdata(indexed_data)

    tm = TimeSeriesConstructor(indexed_data)
    print('construct slices')
    X,y = tm.construct_slices()
    printSlices(X, y)
    print('normalizing')
    n_features=len(X[0][0])
    model = Sequential()
    n_steps = 4
    test_X, test_y, train_X, train_y = tm.cross_validation(X, y)
    model.add(LSTM(600, activation='relu', return_sequences=True, input_shape=(n_steps, n_features)))
    model.add(LSTM(600, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mae')
    model.fit(np.array(train_X), np.array(train_y),epochs=3)

    y_predicted = model.predict(np.array(test_X))
    mae = np.array([abs(x[0]-y) for (x,y) in zip(y_predicted,test_y)]).mean()
    print(f'mae: {mae}')
