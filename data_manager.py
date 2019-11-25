from sklearn.preprocessing import *
from datetime import datetime
import numpy as np
import math

class DataManager(object):
    """
    This Class can be used to manage all aspects of data
    """

    def __init__(self, data, indexes):
        """
        Initialize the internal state of the sample list to X.

        :param X: list of samples.
        """
        self.data = data.copy()
        self.nom_indexes = indexes
        self.num_indexes = [x for x in range(len(self.data[0])) if x not in self.nom_indexes]
        self.attributes = dict()
        for i in indexes:
            values = set()
            for v in self.data:
                values.add(v[i])
            self.attributes.setdefault(i, list(values))

    def nominalToNumeric(self, data=None, indexes=None):
        """
        Converts nominal attributes into numeric attributes.

        :param indexes: indexes of the attribute to convert
        :return: the list of samples converted.
        """

        if data is not None:
            self.data = data.copy()

        if indexes is not None:
            self.nom_indexes = indexes

        for x in self.data:
            for i in self.nom_indexes:
                try:
                    x[i] = float(self.attributes.get(i).index(x[i])) + 1
                except:
                    pass

        return self.data.copy()

    def numericToNominal(self, data=None, indexes=None):
        """
        Converts numeric attributes into nominal attributes.

        :param indexes: indexes of the attribute to convert
        :return: the list of samples converted.
        """

        if data is not None:
            self.data = data.copy()

        if indexes is not None:
            self.nom_indexes = indexes

        for x in self.data:
            for i in self.nom_indexes:
                try:
                    x[i] = self.attributes[i][int(x[i] - 1)]
                except:
                    pass

        return self.data.copy()

    def normalize(self, data=None, indexes=None, method=normalize, **kwargs):

        if data is not None:
            self.data = data.copy()

        if indexes is not None:
            self.num_indexes = indexes
            ar = np.arange(len(self.data[0]))
            self.nom_indexes = [x for x in ar if x not in indexes]

        X1 = np.array(self.data.copy())
        try:
            X2 = method(X1[:, self.num_indexes], **kwargs)
            result = np.concatenate((X1[:, self.nom_indexes], X2), axis=1)
            self.data = list(result)
        except:
            print('failed normalization by indexes.')

        return self.data.copy()


class TimeSeriesConstructor(object):
    def __init__(self, data, user_index=0, time_index=1):
        self.data = data.copy()
        self.user_index = user_index
        self.time_index = time_index
        X = []
        userid = self.data[0][user_index]
        slice = []
        for i in range(len(self.data)):
            if self.data[i][user_index] == userid:
                slice.append(self.data[i])
            else:
                X.append(slice)
                slice = [self.data[i]]
                userid = self.data[i][user_index]
        self.timeseries = X

    def timeDiffinDays(self, first, second):
        date_format = "%Y-%m-%d"  #"%d/%m/%Y"
        a = datetime.strptime(first, date_format)
        b = datetime.strptime(second, date_format)
        if a > b:
            delta = a - b
        else:
            delta = b - a
        return delta.days

    def construct(self, slice_dim=4):
        output = []
        account_transactions = self.timeseries.copy()
        for transactions in account_transactions:
            if len(transactions) >= slice_dim:
                date = transactions[0][self.time_index]
                slice = []
                for i in range(len(transactions)):
                    trans = transactions[i]
                    temp = trans[self.time_index]
                    trans[self.time_index] = self.timeDiffinDays(temp,date)
                    date = temp
                    slice.append(trans)
                    if len(slice) == slice_dim:
                        output.append(slice.copy())
                        slice = []
        return output

