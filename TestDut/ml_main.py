from tsai.all import *
computer_setup()

#
import pandas as pd
import numpy as np

#
import pprint


#
ucr_multivariate_list = get_UCR_multivariate_list()
len_ucr_multivariate_list = len(ucr_multivariate_list)
print(ucr_multivariate_list)
print(len_ucr_multivariate_list)

#
in_filename = 'csv/dump.3342867.csv'

#
def foo_bar(x):
    if x == 'x':
        return 0

    if x.startswith('b'):
        if x == 'bx':
            return 0
        
        ret = int(x[1:], 2)
        return ret

    try:
        iv = int(x)
        return iv
    except:
        return x

    return None

#
df = pd.read_csv(in_filename)
df = df.applymap(foo_bar)

#
dsid = 'NATOPS' 
X, y, splits = get_UCR_data(dsid, return_split=False)

print(X.shape)
print(y.shape)
print(splits)



#
signal_times = np.array([int(_item) for _item in list(df.columns)[2:]], dtype=np.int32)
len_signal_times = len(signal_times)
print(f'(#{len_signal_times}) {signal_times}')

time_list = list(range(len_signal_times))
print(f'(#{len_signal_times}) {time_list}')


#
signals = list(df.index)
len_signals = len(signals)
print(f'(#{len_signals}) {signals}')


#
X = []
X.append([])
for row_index in range(len_signals):
    row = np.array(df.iloc[row_index].values[2:], dtype=np.int32)
    X[0].append(row)
X[0].append(signal_times)

#
pprint.pprint(X)

#
y = [1] * len_signal_times

#
splits = []

# train times
splits.append([0])


#
for dump_index in range(len(splits[0])):
    print(f'dump = {splits[0][dump_index]}')
    for time_index in range(len_signal_times):
        for signal_index in range(len_signals):
            print(f'  value[signal{signal_index}][time{time_index}]={X[0][signal_index][time_index]}')
    print(f'answer[{dump_index}] = {y[dump_index]}')

##
#for v_time in range(len_signal_times):
#    t1 = splits[0][v_time]
#    t3 = y[v_time]
#    print(f'time={t1}')
#    for v_signal in range(len_signals):
#        t2 = X[0][v_signal][v_time]
#        print(f'  time={t1}, value[signal{v_signal}][time{v_time}]={t2}, answer={t3}')
#    print(f'answer={t3}')


##
#learn = TSClassifier(X, y, splits=splits, bs=[64, 128], batch_tfms=[TSStandardize()], arch=InceptionTime, metrics=accuracy)
#learn.fit_one_cycle(25, lr_max=1e-3)
#learn.plot_metrics()

tfms  = [None, [Categorize()]]
dsets = TSDatasets(X, y, tfms=tfms, splits=splits, inplace=True)
dls   = TSDataLoaders.from_dsets(dsets.train, dsets.valid, bs=[64, 128], batch_tfms=[TSStandardize()], num_workers=0)
model = InceptionTime(dls.vars, dls.c)
learn = Learner(dls, model, metrics=accuracy)
learn.fit_one_cycle(25, lr_max=1e-3)
learn.plot_metrics()


#
pprint.pprint(df)