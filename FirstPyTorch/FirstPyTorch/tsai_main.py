from tsai.all import *
computer_setup()

#
import tsai_read_csv

#
import numpy as np

#
import pprint

#
import glob

#
def debug_print(X, y, splits):
    for dump_index in range(len(splits[0])):
        print(f'dump = {splits[0][dump_index]}')
        for time_index in range(len_signal_times):
            for signal_index in range(len_signals):
                print(f'  value[signal{signal_index}][time{time_index}]={X[0][signal_index][time_index]}')
        print(f'answer[{dump_index}] = {y[dump_index]}')

##
#ucr_multivariate_list = get_UCR_multivariate_list()
#len_ucr_multivariate_list = len(ucr_multivariate_list)
#print(ucr_multivariate_list)
#print(len_ucr_multivariate_list)


##
#learn = TSClassifier(X, y, splits=splits, bs=[64, 128], batch_tfms=[TSStandardize()], arch=InceptionTime, metrics=accuracy)
#learn.fit_one_cycle(25, lr_max=1e-3)
#learn.plot_metrics()


#
csv_filenames = glob.glob('csv/dump.*.csv')


#
randomized_filenames = random_shuffle(csv_filenames)
train_filenames = randomized_filenames[:100]
test_filenames = randomized_filenames[100:200]


##
#train_filenames = ['csv/dump.3342867.csv',]
#test_filenames = ['csv/dump.3342867.csv',]

## fails
#train_filenames = ['csv\\dump.1496808330.csv',  'csv\\dump.588072216.csv',   'csv\\dump.-1619294067.csv', 'csv\\dump.1832790533.csv',]
#test_filenames  = ['csv\\dump.-1007886330.csv', 'csv\\dump.1560800731.csv',  'csv\\dump.-603251626.csv',  'csv\\dump.1440514764.csv',]
#train_filenames = ['csv\\dump.-1362792616.csv', 'csv\\dump.-1479646853.csv', 'csv\\dump.-961495142.csv',  'csv\\dump.-2014888715.csv']
#test_filenames  = ['csv\\dump.-232455159.csv',  'csv\\dump.-1406558288.csv', 'csv\\dump.817053858.csv',   'csv\\dump.-920560961.csv']
#train_filenames = ['csv\\dump.540591740.csv',   'csv\\dump.1404258344.csv',  'csv\\dump.1275220518.csv',  'csv\\dump.2080562704.csv']
#test_filenames  = ['csv\\dump.-589694738.csv',  'csv\\dump.1218321297.csv',  'csv\\dump.-618488600.csv',  'csv\\dump.-1240460371.csv']

## pass
#train_filenames = ['csv\\dump.711500353.csv',   'csv\\dump.1398169190.csv',  'csv\\dump.-2079575350.csv', 'csv\\dump.508593244.csv']
#test_filenames  = ['csv\\dump.-467270794.csv',  'csv\\dump.871963389.csv',   'csv\\dump.2080211657.csv',  'csv\\dump.-1673208017.csv']
#train_filenames = ['csv\\dump.-236213973.csv',  'csv\\dump.133767574.csv',   'csv\\dump.-247709426.csv',  'csv\\dump.1137226842.csv']
#test_filenames  = ['csv\\dump.1691562744.csv',  'csv\\dump.-1781733962.csv', 'csv\\dump.-1184192299.csv', 'csv\\dump.755844384.csv']
#train_filenames = ['csv\\dump.-1946293147.csv', 'csv\\dump.-941985772.csv',  'csv\\dump.-444007488.csv',  'csv\\dump.66716960.csv']
#test_filenames  = ['csv\\dump.1441146131.csv',  'csv\\dump.1107110238.csv',  'csv\\dump.947301770.csv',   'csv\\dump.-58236041.csv']




#
dsid = 'NATOPS' 
X1, y1, splits1 = get_UCR_data(dsid, return_split=False)
X2, y2, splits2 = tsai_read_csv.read_from_csv(
        train_filenames=train_filenames,
        test_filenames=test_filenames,
    )

##
#tfms1  = [None, [Categorize()]]
#dsets1 = TSDatasets(X1, y1, tfms=tfms1, splits=splits1, inplace=True)
#dls1   = TSDataLoaders.from_dsets(dsets1.train, dsets1.valid, bs=[64, 128], batch_tfms=[TSStandardize()], num_workers=0)
#model1 = InceptionTime(dls1.vars, dls1.c)
#learn1 = Learner(dls1, model1, metrics=accuracy)
#learn1.fit_one_cycle(25, lr_max=1e-3)
#learn1.plot_metrics()

#
tfms2  = [None, [Categorize()]]
dsets2 = TSDatasets(X2, y2, tfms=tfms2, splits=splits2, inplace=True)
dls2   = TSDataLoaders.from_dsets(dsets2.train, dsets2.valid, bs=[64, 128], batch_tfms=[TSStandardize()], num_workers=0)
model2 = InceptionTime(dls2.vars, dls2.c)
learn2 = Learner(dls2, model2, metrics=accuracy)
learn2.fit_one_cycle(25, lr_max=1e-3)
learn2.plot_metrics()


#
print('''let's compare''')