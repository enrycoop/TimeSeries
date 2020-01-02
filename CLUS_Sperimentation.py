import subprocess
from random import seed
from random import randint


def split_files(path, iter, n_train):
    with open(path, 'r') as fl:
        lines = fl.readlines()
    intest = lines[:lines.index('@data\n')+1]
    data = lines[lines.index('@data\n')+1:]
    set_indexes = set()
    while len(set_indexes) < n_train:
        set_indexes.add(randint(0, len(data)))
    train = []
    test = []
    for i in range(len(data)):
        if i in set_indexes:
            train.append(data[i])
        else:
            test.append(data[i])
    with open(f'resources/{iter}/train{n_train}.arff', 'w') as fl:
        fl.writelines(intest)
        fl.writelines(train)
    with open(f'resources/{iter}/test{n_train}.arff', 'w') as fl:
        fl.writelines(intest)
        fl.writelines(test)
    separator = ','

    for i in range(len(test)):
        y = test[i].split(',')
        y[2] = '?'
        test[i] = separator.join(y)
    with open(f'resources/{iter}/unlabeled{n_train}.arff', 'w') as fl:
        fl.writelines(intest)
        fl.writelines((test))


def set_conf_file(path,i,n_examples):
    with open(path, 'r') as fl:
        lines = fl.readlines()
    lines[lines.index('[Data]\n')+1] = f'File = resources/{i}/train{n_examples}.arff\n'
    lines[lines.index('[Data]\n') + 2] = f'TestSet = resources/{i}/test{n_examples}.arff\n'
    lines[lines.index('[SemiSupervised]\n') + 1] = f'UnlabeledData = resources/{i}/unlabeled{n_examples}.arff\n'
    with open(f'external_libraries/conf.s', 'w') as fl:
        fl.writelines(lines)


def extract_statistics(path, first='   Original       : [',indexes=(6,10,14,22)):
    with open(path, 'r') as fl:
        lines = fl.readlines()
    lines = lines[lines.index('Testing error\n'):]
    mae = float(lines[indexes[0]].replace(first,'').replace(']\n',''))
    mse = float(lines[indexes[1]].replace(first,'').replace(']\n',''))
    rmse = float(lines[indexes[2]].replace(first, '').replace(']\n', ''))
    rrmse = float(lines[indexes[3]].replace(first,'').replace(']\n',''))
    return mae, mse, rmse, rrmse

#, first='   Forest with 100 trees: ['
# indexes=(7,11,15,23)


if __name__ == '__main__':
    seed()
    sizes = [5000,3500]
    n = 10

    for i in sizes:
        maes = 0
        mses = 0
        rmses = 0
        rrmses = 0
        with open(f'ssl_rf{i}.csv', 'w') as ssl_pct:
            ssl_pct.write('mae;mse;rmse;rrmse\n')
            for j in range(n):
                set_conf_file('external_libraries/conf.s', j, i)
                subprocess.run(['java', '-jar', '-Xmx4048m', 'external_libraries/clusSSL.jar','-forest','-ssl', f'external_libraries/conf.s'])
                mae, mse, rmse, rrmse = extract_statistics('external_libraries/conf.out',indexes=(6,9,12,18))
                maes += mae
                mses += mse
                rmses += rmse
                rrmses += rrmse
                ssl_pct.write(f'{mae};{mse};{rmse};{rrmse}\n')
            ssl_pct.write(f'{maes/n};{mses/n};{rmses/n};{rrmses/n}\n')
