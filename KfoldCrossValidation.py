from data_manager import *
from data_access import *


if __name__ == '__main__':
    X = DatabaseWrapper().getAllTransactions()
    sep = ','
    date = X[0][1]
    id = X[0][0]
    lines = []
    for x in X[:1000]:
        if x[0] == id:
            days = timeDiffinDays(x[1],date)
            date = x[1]
            x[1] = days
        else:
            id = x[0]
            date = x[1]
            x[1] = 0
        lines.append(f"{x[0]},{x[1]},{x[2]},'{x[3]}','{x[4]}','{x[5]}'\n")
    with open('trans.csv','w') as f:
        f.writelines(lines)